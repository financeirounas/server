from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    id: str = Field(..., description="Identificador único do pedido")
    description: Optional[str] = Field(None, description="Descrição do pedido")
    amount: Optional[float] = Field(None, description="Quantidade do pedido")
    unit_id: Optional[str] = Field(None, description="Identificador da unidade")
    budget_id: Optional[str] = Field(None, description="Identificador do orçamento")
    status: Optional[str] = Field(None, description="Status do pedido (pending, approved, rejected, completed)")
    created_at: datetime = Field(..., description="Data de criação")