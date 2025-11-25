from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id : str = Field(..., description="Identificador único do usuário")
    email: EmailStr = Field(..., description="E-mail institucional do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")
    username: str = Field(..., description="Nome de usuário")
    type: str = Field(..., description="Tipo de usuário (e.g., admin, regular)")