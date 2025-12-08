from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as date_type

class BudgetCreateDTO(BaseModel):
    description: str = Field(..., description="Descrição do orçamento")
    initial_date: date_type = Field(..., description="Data inicial do orçamento")
    final_date: date_type = Field(..., description="Data final do orçamento")
    amount: float = Field(..., description="Valor total do orçamento")

class BudgetUpdateDTO(BaseModel):
    description: Optional[str] = Field(None, description="Descrição do orçamento")
    initial_date: Optional[date_type] = Field(None, description="Data inicial do orçamento")
    final_date: Optional[date_type] = Field(None, description="Data final do orçamento")
    amount: Optional[float] = Field(None, description="Valor total do orçamento")

class BudgetResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do orçamento")
    description: str = Field(..., description="Descrição do orçamento")
    initial_date: date_type = Field(..., description="Data inicial do orçamento")
    final_date: date_type = Field(..., description="Data final do orçamento")
    amount: float = Field(..., description="Valor total do orçamento")
    created_at: str = Field(..., description="Data de criação do orçamento")
    updated_at: Optional[str] = Field(None, description="Data de atualização do orçamento")