from typing import List, Optional
from fastapi import HTTPException
from lib.supabase_client import supabase
from entities.models.frequency import Frequency
from datetime import date, datetime

class FrequencyRepository:
    TABLE_NAME = "frequency"

    @staticmethod
    async def list_frequencies(
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        unit_id: Optional[str] = None,
    ) -> List[Frequency]:
        """
        Lista todas as frequências, com filtros opcionais por período e unidade.
        Retorna lista de Frequency.
        """
        query = supabase.table(FrequencyRepository.TABLE_NAME).select("*")

        if initial_date:
            query = query.gte("date", initial_date)
        if final_date:
            query = query.lte("date", final_date)
        if unit_id:
            query = query.eq("unit_id", unit_id)

        response = query.execute()

        if not response.data:
            return []

        def _normalize(item: dict) -> dict:
            amount = item.get("amount") or item.get("quantity") or 0
            # Converte date para objeto date do Python se for string
            date_value = item.get("date")
            if isinstance(date_value, str):
                try:
                    date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
                except:
                    pass
            elif isinstance(date_value, datetime):
                date_value = date_value.date()
            
            normalized = {
                "id": item.get("id"),
                "unit_id": item.get("unit_id"),
                "amount": amount,
                "date": date_value,
                "updated_at": item.get("updated_at"),
            }
            return normalized

        return [Frequency(**_normalize(item)) for item in response.data]
    
    @staticmethod
    async def get_frequency_by_id(frequency_id: str) -> Frequency:
        """
        Busca uma frequência pelo ID.
        Retorna o registro encontrado.
        """
        response = (
            supabase.table(FrequencyRepository.TABLE_NAME)
            .select("*")
            .eq("id", frequency_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Frequência não encontrada")

        item = response.data[0]
        amount = item.get("amount") or item.get("quantity") or 0
        
        # Converte date para objeto date do Python se for string
        date_value = item.get("date")
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
            except:
                pass
        elif isinstance(date_value, datetime):
            date_value = date_value.date()
        
        return Frequency(
            id=item.get("id"),
            unit_id=item.get("unit_id"),
            amount=amount,
            date=date_value,
            updated_at=item.get("updated_at"),
        )
    
    @staticmethod
    async def create_frequency(data: dict) -> Frequency:
        """
        Cria uma nova frequência.
        Valida se já existe frequência para a mesma unidade no mesmo dia.
        Retorna o registro criado.
        """
        # Verifica se já existe frequência para esta unidade neste dia
        unit_id = data.get("unit_id")
        freq_date = data.get("date")
        
        if unit_id and freq_date:
            existing = (
                supabase.table(FrequencyRepository.TABLE_NAME)
                .select("*")
                .eq("unit_id", unit_id)
                .eq("date", freq_date)
                .execute()
            )
            if existing.data:
                raise HTTPException(
                    status_code=409, 
                    detail=f"Já existe uma frequência registrada para esta unidade no dia {freq_date}"
                )
        
        response = (
            supabase.table(FrequencyRepository.TABLE_NAME)
            .insert(data)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar frequência")

        item = response.data[0]
        amount = item.get("amount") or item.get("quantity") or 0
        
        # Converte date para objeto date do Python se for string
        date_value = item.get("date")
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
            except:
                pass
        elif isinstance(date_value, datetime):
            date_value = date_value.date()
        
        return Frequency(
            id=item.get("id"),
            unit_id=item.get("unit_id"),
            amount=amount,
            date=date_value,
            updated_at=item.get("updated_at"),
        )
    
    @staticmethod
    async def update_frequency(frequency_id: str, data: dict) -> Frequency:
        """
        Atualiza uma frequência existente.
        Retorna o registro atualizado.
        """
        response = (
            supabase.table(FrequencyRepository.TABLE_NAME)
            .update(data)
            .eq("id", frequency_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar frequência")

        item = response.data[0]
        amount = item.get("amount") or item.get("quantity") or 0
        
        # Converte date para objeto date do Python se for string
        date_value = item.get("date")
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
            except:
                pass
        elif isinstance(date_value, datetime):
            date_value = date_value.date()
        
        return Frequency(
            id=item.get("id"),
            unit_id=item.get("unit_id"),
            amount=amount,
            date=date_value,
            updated_at=item.get("updated_at"),
        )
    
    @staticmethod
    async def delete_frequency(frequency_id: str) -> None:
        """
        Deleta uma frequência pelo ID.
        """
        response = (
            supabase.table(FrequencyRepository.TABLE_NAME)
            .delete()
            .eq("id", frequency_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao deletar frequência")