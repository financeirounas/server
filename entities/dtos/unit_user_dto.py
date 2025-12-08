from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UnitUserResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único da relação unidade-usuário")
    unit_id: str = Field(..., description="Identificador único da unidade")
    user_id: str = Field(..., description="Identificador único do usuário")
    role: str = Field(..., description="Papel do usuário na unidade (e.g., gestor, colaborador)")
    created_at: Optional[str] = Field(None , description="Data e hora em que o usuário foi atribuído à unidade")
    updated_at: Optional[str] = Field(None, description="Data e hora da última atualização da relação unidade-usuário")

class UnitUserCreateDTO(BaseModel):
    unit_id: str = Field(..., description="Identificador único da unidade")
    user_id: str = Field(..., description="Identificador único do usuário")
    role: str = Field(..., description="Papel do usuário na unidade (e.g., gestor, colaborador)")


class UnitUserUpdateDTO(BaseModel):
    role: Optional[str] = Field(None, description="Papel do usuário na unidade (e.g., gestor, colaborador)")
