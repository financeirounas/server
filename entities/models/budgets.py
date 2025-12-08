from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class Budget(BaseModel):
    id: str = Field(..., description="Identificador único do orçamento")
    description: str = Field(..., description="Descrição do orçamento")
    initial_date: date = Field(..., description="Data inicial do orçamento")
    final_date: date = Field(..., description="Data final do orçamento")
    amount: float = Field(..., description="Valor total do orçamento")
    created_at: datetime = Field(..., description="Data de criação do orçamento")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização do orçamento")