from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as date_type

class FrequencyCreateDTO(BaseModel):
    unit_id: str = Field(..., description="Identificador da unidade associada")
    amount: int = Field(..., description="Quantidade")
    date: date_type = Field(..., description="Data da frequência")

class FrequencyUpdateDTO(BaseModel):
    amount: Optional[int] = Field(None, description="Quantidade")
    date: Optional[date_type] = Field(None, description="Data da frequência")

class FrequencyResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único da frequência")
    unit_id: str = Field(..., description="Identificador da unidade associada")
    amount: int = Field(..., description="Quantidade")
    date: Optional[str] = Field(..., description="Data da frequência")
    updated_at: Optional[str] = Field(None, description="Data e hora da última atualização")