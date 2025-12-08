from pydantic import BaseModel, Field
from typing import Optional

class UnitCreateDTO(BaseModel):
    name: str = Field(..., description="Nome da unidade")
    address: str = Field(..., description="Endereço da unidade")
    type: str = Field(..., description="Tipo da unidade")
    capacity: Optional[int] = Field(None, description="Capacidade (número de pessoas)")

class UnitUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, description="Nome da unidade")
    address: Optional[str] = Field(None, description="Endereço da unidade")
    type: Optional[str] = Field(None, description="Tipo da unidade")
    capacity: Optional[int] = Field(None, description="Capacidade (número de pessoas)")

class UnitResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único da unidade")
    name: Optional[str] = Field(None, description="Nome da unidade")
    address: Optional[str] = Field(None, description="Endereço da unidade")
    type: Optional[str] = Field(None, description="Tipo da unidade")
    capacity: Optional[int] = Field(None, description="Capacidade da unidade")
    created_at: str = Field(..., description="Data de criação")
    updated_at: Optional[str] = Field(None, description="Data de atualização")