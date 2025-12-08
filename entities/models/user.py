from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str = Field(..., description="Identificador único do usuário")
    email: EmailStr = Field(..., description="E-mail institucional do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")
    username: str = Field(..., description="Nome de usuário")
    role: str = Field(..., description="Tipo de usuário (e.g., admin, regular)")
    active: Optional[bool] = Field(True, description="Se o usuário está ativo (soft delete)")
    email_verified: Optional[bool] = Field(False, description="Se o e-mail foi verificado")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None