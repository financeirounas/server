from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrderItem(BaseModel):
    id: str = Field(..., description="Identificador único do item")
    description: Optional[str] = Field(None, description="Descrição do item")
    amount: float = Field(..., description="Quantidade do item")
    measure_unit: str = Field(default="pacote", description="Unidade de medida")
    received: bool = Field(default=True, description="Indica se o item foi recebido")
    order_id: str = Field(..., description="Identificador do pedido")
    created_at: datetime = Field(..., description="Data de criação")