from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ReportMetrics(BaseModel):
    capacity: Optional[int] = Field(None, description="Capacidade total da unidade")
    frequency_pct: Optional[float] = Field(None, description="Frequência atual em porcentagem (0-100)")
    cost_per_capita: Optional[float] = Field(None, description="Custo por pessoa no período")
    total_spending: Optional[float] = Field(None, description="Gasto total no período (raw)")

class ReportTotals(BaseModel):
    packs_budget: Optional[int] = Field(None, description="Número de pacotes provenientes da verba/compras")
    packs_donations: Optional[int] = Field(None, description="Número de pacotes provenientes de doações")
    total_packs: Optional[int] = Field(None, description="Total de pacotes")
    packs_consumed: Optional[int] = Field(None, description="Pacotes consumidos no período (se disponível)")

class StorageSummary(BaseModel):
    food: str = Field(..., description="Nome do alimento/categoria")
    bought_amount: float = Field(0.0, description="Quantidade comprada (na unidade original, ex: kg, L, pacotes)")
    donated_amount: float = Field(0.0, description="Quantidade doada")
    total_amount: float = Field(0.0, description="Soma de comprado + doado")
    measure_unit: Optional[str] = Field(None, description="Unidade de medida (kg, L, pacotes)")

class OrderSummary(BaseModel):
    id: str
    date: Optional[datetime]
    amount: float
    items_count: Optional[int] = None

class FrequencySummary(BaseModel):
    id: str = Field(..., description="ID da frequência")
    unit_id: str = Field(..., description="ID da unidade")
    amount: int = Field(..., description="Quantidade")
    date: str = Field(..., description="Data da frequência (formatada dd/mm/YYYY HH:MM)")

class MonthlyComparison(BaseModel):
    month: str  # "2025-10"
    budget: Optional[float] = None
    spent: Optional[float] = None

class ReportByUnit(BaseModel):
    unit_id: str
    unit_name: str
    month: Optional[str] = Field(None, description="Período do relatório no formato YYYY-MM (opcional)")
    generated_at: datetime
    metrics: ReportMetrics
    totals: ReportTotals
    storage_summary: List[StorageSummary] = []
    monthly_comparison: List[MonthlyComparison] = []
    recent_orders: List[OrderSummary] = []
    frequencies: List[FrequencySummary] = []
