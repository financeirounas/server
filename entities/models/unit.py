from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Unit(BaseModel):
    id: str = Field(..., description="Identificador único da unidade")
    name: Optional[str] = Field(None, description="Nome da unidade")
    address: Optional[str] = Field(None, description="Endereço da unidade")
    type: Optional[str] = Field(None, description="Tipo da unidade")
    capacity: Optional[int] = Field(None, description="Capacidade (número de pessoas)")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")