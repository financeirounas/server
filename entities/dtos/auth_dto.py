from pydantic import BaseModel, EmailStr, Field

class LoginDTO(BaseModel):
    email: EmailStr = Field(..., description="E-mail institucional do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")


class VerifyEmailDTO(BaseModel):
    code: str = Field(..., description="Token de verificação de e-mail")
    
    
class SendVerifyEmailCodeDTO(BaseModel):
    email: EmailStr = Field(..., description="E-mail institucional do usuário")