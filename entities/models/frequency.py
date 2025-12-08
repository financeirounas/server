from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from datetime import date as date_type

class Frequency(BaseModel):
    id: str = Field(..., description="Identificador único da frequência")
    unit_id: str = Field(..., description="Identificador da unidade associada")
    amount: int = Field(..., description="Quantidade")
    date: date_type = Field(..., description="Data da frequência")
    updated_at: Optional[datetime] = Field(None, description="Data e hora da última atualização")