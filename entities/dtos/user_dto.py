from pydantic import BaseModel, Field
from typing import Optional

class UserUpdateDTO(BaseModel):
    email: Optional[str] = Field(None, description="E-mail institucional do usuário")
    username: Optional[str] = Field(None, description="Nome de usuário")
    role: Optional[str] = Field(None, description="Tipo de usuário (e.g., admin, regular)")

class UserCreateDTO(BaseModel):
    email: str = Field(..., description="E-mail institucional do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")
    username: str = Field(..., description="Nome de usuário")
    role: str = Field(..., description="Tipo de usuário (e.g., admin, regular)")
    id: Optional[str] = Field(None, description="Identificador único do usuário")

class UserResponseDTO(BaseModel):
    id : str = Field(..., description="Identificador único do usuário")
    email: str = Field(..., description="E-mail institucional do usuário")
    username: str = Field(..., description="Nome de usuário")
    role: str = Field(..., description="Tipo de usuário (e.g., admin, regular)")
    units : Optional[list] = Field(None, description="Lista de unidades associadas ao usuário")
