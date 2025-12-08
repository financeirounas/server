# services/reports_service.py
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, date
from zoneinfo import ZoneInfo
from fastapi import HTTPException

from entities.dtos.report_dto import (
    ReportByUnit, ReportMetrics, ReportTotals, StorageSummary,
    OrderSummary, MonthlyComparison, FrequencySummary
)

# Helpers (mantidos localmente)
def parse_month_to_range(month_str: Optional[str]):
    if not month_str:
        return None, None
    try:
        month_str = month_str.strip().strip('"').strip("'")
        parts = month_str.split("-")
        if len(parts) != 2:
            raise ValueError(f"Formato inválido: esperado YYYY-MM, recebido '{month_str}'")
        year, mon = parts
        y = int(year)
        m = int(mon)
        if m < 1 or m > 12:
            raise ValueError(f"Mês inválido: {m}. Deve estar entre 1 e 12.")
        start = date(y, m, 1)
        if m == 12:
            end = date(y + 1, 1, 1)
        else:
            end = date(y, m + 1, 1)
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.min.time())
        return start_dt, end_dt
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=400, detail=f"Parâmetro 'month' inválido: {str(e)}")


def to_naive_datetime(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return None
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime.combine(dt, datetime.min.time())
    if isinstance(dt, datetime):
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt
    return None


class ReportsService:
    """
    Service responsável por montar relatórios por unidade.
    Observação: fazemos imports de outros serviços *dentro* dos métodos para evitar
    circular imports caso esses serviços importem algo deste módulo.
    """

    @staticmethod
    async def generate_unit_report(unit_id: str, month: Optional[str] = None) -> ReportByUnit:
        # Imports feitos localmente para evitar circular imports
        from services.unit_service import UnitService
        from services.storage_service import StorageService
        from services.order_service import OrderService
        from services.budget_service import BudgetService
        from services.unit_user_service import UnitUserService
        from services.frequency_service import FrequencyService

        # 1) validar unidade
        unit = await UnitService.get_unit_by_id(unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        # 2) período: usar month como base inicial
        start_dt, end_dt = parse_month_to_range(month)

        initial_date = start_dt.isoformat() if start_dt else None
        final_date = end_dt.isoformat() if end_dt else None

        freq_initial_date = start_dt.date().isoformat() if start_dt else None
        freq_final_date = end_dt.date().isoformat() if end_dt else None

        # 3) buscar dados em paralelo (os serviços devem suportar os filtros usados)
        tasks = [
            StorageService.get_storage_by_unit(unit_id),
            OrderService.list_orders(unit_id=unit_id),
            BudgetService.list_budgets(initial_date=initial_date, final_date=final_date),
            UnitUserService.list_users_by_unit(unit_id),
            FrequencyService.list_frequencies(initial_date=freq_initial_date, final_date=freq_final_date, unit_id=unit_id)
        ]
        storage_items, orders, budgets, members, frequencies = await asyncio.gather(*tasks)

        # 4) se budgets presentes, ajustar intervalo efetivo do relatório
        actual_start_dt = start_dt
        actual_end_dt = end_dt
        if budgets:
            first_budget = budgets[0]
            budget_initial = getattr(first_budget, "initial_date", None)
            budget_final = getattr(first_budget, "final_date", None)

            if budget_initial:
                try:
                    if isinstance(budget_initial, str):
                        budget_initial = datetime.fromisoformat(budget_initial)
                    else:
                        budget_initial = to_naive_datetime(budget_initial)
                except Exception:
                    budget_initial = None

            if budget_final:
                try:
                    if isinstance(budget_final, str):
                        budget_final = datetime.fromisoformat(budget_final)
                    else:
                        budget_final = to_naive_datetime(budget_final)
                except Exception:
                    budget_final = None

            if budget_initial:
                actual_start_dt = budget_initial
            if budget_final:
                actual_end_dt = budget_final

        # 5) filtrar orders por intervalo efetivo
        filtered_orders = []
        for o in (orders or []):
            created = getattr(o, "created_at", None)
            created = to_naive_datetime(created)
            if actual_start_dt and actual_end_dt:
                if created and (created >= actual_start_dt and created < actual_end_dt):
                    filtered_orders.append(o)
            else:
                filtered_orders.append(o)

        # 6) total_spending (soma dos orders filtrados)
        total_spending = 0.0
        for o in filtered_orders:
            amt = getattr(o, "amount", 0) or 0
            try:
                total_spending += float(amt)
            except Exception:
                pass

        # 7) storage summary: agrupar por (name, measure_unit) usando initial/used/current
        storage_map: Dict[str, Dict[str, float]] = {}
        for s in (storage_items or []):
            name = getattr(s, "name", "Desconhecido")
            origin = getattr(s, "type", "") or ""
            initial_q = float(getattr(s, "initial_quantity", 0) or 0)
            used_q = float(getattr(s, "used_quantity", 0) or 0)
            current_q = max(0.0, initial_q - used_q)
            measure_unit = getattr(s, "measure_unit", None) or getattr(s, "measureUnit", None) or None

            key_str = f"{name}||{measure_unit or ''}"
            if key_str not in storage_map:
                storage_map[key_str] = {
                    "name": name,
                    "measure_unit": measure_unit,
                    "bought": 0.0,
                    "donated": 0.0,
                    "current": 0.0
                }

            if isinstance(origin, str) and origin.lower().startswith("doa"):
                storage_map[key_str]["donated"] += initial_q
            else:
                storage_map[key_str]["bought"] += initial_q

            storage_map[key_str]["current"] += current_q

        storage_summary: List[StorageSummary] = []
        for v in storage_map.values():
            total_amt = v["bought"] + v["donated"]
            storage_summary.append(StorageSummary(
                food=v["name"],
                bought_amount=v["bought"],
                donated_amount=v["donated"],
                total_amount=total_amt,
                measure_unit=v["measure_unit"]
            ))

        # packs heuristics (usar current para pacotes)
        packs_budget = 0
        packs_donations = 0
        for v in storage_map.values():
            mu = (v["measure_unit"] or "").lower()
            if "pacote" in mu or "pacotes" in mu or mu == "":
                # contagem conservadora baseada em current
                current_as_int = int(round(v["current"]))
                # estimativa de origem por proporção
                denom = (v["bought"] + v["donated"]) or 1.0
                if denom > 0:
                    bought_prop = (v["bought"] / denom) if denom else 0.0
                    donated_prop = (v["donated"] / denom) if denom else 0.0
                    packs_budget += int(round(current_as_int * bought_prop))
                    packs_donations += int(round(current_as_int * donated_prop))

        total_packs = sum(
            int(round(v["current"])) if ((v.get("measure_unit") or "").lower().find("pacote") != -1 or (v.get("measure_unit") or "") == "")
            else 0
            for v in storage_map.values()
        )

        totals = ReportTotals(
            packs_budget=packs_budget if packs_budget > 0 else None,
            packs_donations=packs_donations if packs_donations > 0 else None,
            total_packs=total_packs if total_packs > 0 else None,
            packs_consumed=None
        )

        # 8) metrics
        capacity = getattr(unit, "capacity", None)
        try:
            if capacity is not None and not isinstance(capacity, (int, float)):
                capacity = int(str(capacity))
        except Exception:
            capacity = None

        frequency_pct = 0.0
        avg_attendance = 0.0
        try:
            freqs = frequencies or []
            counts = [float(getattr(f, "amount", 0) or 0) for f in freqs]
            if counts:
                avg_attendance = sum(counts) / len(counts)
                if capacity and capacity > 0:
                    frequency_pct = ((avg_attendance / float(capacity)) * 100.0)
        except Exception:
            frequency_pct = 0.0
            avg_attendance = 0.0

        budget_total = 0.0
        try:
            budget_total = sum(float(getattr(b, "amount", 0) or 0) for b in (budgets or []))
        except Exception:
            budget_total = 0.0

        if capacity and capacity > 0:
            try:
                cost_per_capita = budget_total / float(capacity)
            except Exception:
                cost_per_capita = 0.0
        else:
            cost_per_capita = 0.0

        metrics = ReportMetrics(
            capacity=capacity,
            frequency_pct=frequency_pct,
            cost_per_capita=cost_per_capita,
            total_spending=total_spending
        )

        # 9) recent orders
        order_summaries: List[OrderSummary] = []
        def order_key(o):
            created = getattr(o, "created_at", None)
            created = to_naive_datetime(created)
            return created or datetime.min

        sorted_orders = sorted(filtered_orders, key=order_key, reverse=True)[:10]
        for o in sorted_orders:
            created = getattr(o, "created_at", None)
            created = to_naive_datetime(created)
            items = getattr(o, "items", None)
            items_count = len(items) if isinstance(items, (list, tuple)) else getattr(o, "items_count", None)
            order_summaries.append(OrderSummary(
                id=str(getattr(o, "id", "")),
                date=created,
                amount=float(getattr(o, "amount", 0) or 0),
                items_count=items_count
            ))

        # 10) monthly comparison
        month_map: Dict[str, Dict[str, float]] = {}
        for b in (budgets or []):
            bd = getattr(b, "initial_date", None) or getattr(b, "month", None)
            if bd:
                bd_dt = to_naive_datetime(bd)
                if bd_dt:
                    bd_date = bd_dt.date()
                    key = f"{bd_date.year:04d}-{bd_date.month:02d}"
                    month_map.setdefault(key, {"budget": 0.0, "spent": 0.0})
                    month_map[key]["budget"] += float(getattr(b, "amount", 0) or 0)

        all_orders_to_count = filtered_orders  # usa apenas pedidos do mês filtrado

        for o in all_orders_to_count:
            created = getattr(o, "created_at", None)
            created_dt = to_naive_datetime(created)
            if created_dt:
                key = f"{created_dt.year:04d}-{created_dt.month:02d}"
                month_map.setdefault(key, {"budget": 0.0, "spent": 0.0})
                month_map[key]["spent"] += float(getattr(o, "amount", 0) or 0)

        monthly_comparison: List[MonthlyComparison] = []
        for k in sorted(month_map.keys()):
            monthly_comparison.append(MonthlyComparison(month=k, budget=month_map[k]["budget"], spent=month_map[k]["spent"]))

        # 11) frequency summaries
        frequency_summaries: List[FrequencySummary] = []
        for freq in (frequencies or []):
            freq_id = getattr(freq, "id", "")
            freq_unit_id = getattr(freq, "unit_id", "")
            freq_amount = getattr(freq, "amount", 0)
            freq_date = getattr(freq, "date", "")
            frequency_summaries.append(FrequencySummary(
                id=str(freq_id),
                unit_id=str(freq_unit_id),
                amount=freq_amount,
                date=str(freq_date)
            ))

        # 12) montar relatório final
        generated_at = datetime.now(ZoneInfo("America/Sao_Paulo"))
        report = ReportByUnit(
            unit_id=str(getattr(unit, "id", unit_id)),
            unit_name=str(getattr(unit, "name", "")),
            month=month,
            generated_at=generated_at,
            metrics=metrics,
            totals=totals,
            storage_summary=storage_summary,
            monthly_comparison=monthly_comparison,
            recent_orders=order_summaries,
            frequencies=frequency_summaries
        )
        
        print(report.metrics)

        return report
