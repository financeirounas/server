from pydantic import BaseModel, EmailStr, Field

class SecurityCode(BaseModel):
    id : str = Field(..., description="Identificador único do usuário")
    code: str = Field(..., description="Código de segurança gerado")
    user_id: str = Field(..., description="Identificador do usuário associado ao código")
    type: str = Field(..., description="Tipo de código de segurança (e.g., email_verification, password_reset)")
    revoked: bool = Field(..., description="Indica se o código foi revogado")