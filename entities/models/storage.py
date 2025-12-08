from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Storage(BaseModel):
    id: str = Field(..., description="Identificador único do item de estoque")
    amount: float = Field(..., description="Quantidade atual disponível")
    unit_id: str = Field(..., description="Identificador da unidade")
    type: str = Field(..., description="Tipo de entrada (comprado ou doado)")
    name: str = Field(..., description="Nome do item")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")
    initial_quantity: int = Field(..., description="Quantidade inicial do item no estoque")
    used_quantity: int = Field(..., description="Quantidade já utilizada do item no estoque") 

