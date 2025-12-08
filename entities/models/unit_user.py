from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UnitUser(BaseModel):
    id: str = Field(..., description="Identificador único da relação unidade-usuário")
    unit_id: str = Field(..., description="Identificador único da unidade")
    user_id: str = Field(..., description="Identificador único do usuário")
    role: str = Field(..., description="Papel do usuário na unidade (e.g., gestor, colaborador)")
    created_at: Optional[datetime] = Field(None, description="Data e hora em que o usuário foi atribuído à unidade")
    updated_at: Optional[datetime] = Field(None, description="Data e hora da última atualização da relação unidade-usuário")