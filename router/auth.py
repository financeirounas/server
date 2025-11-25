from fastapi import APIRouter, HTTPException
from services.auth_service import AuthService
from entities.dtos.auth_dto import LoginDTO, SendVerifyEmailCodeDTO, VerifyEmailDTO

router = APIRouter()

@router.post("/login")
async def login(dto: LoginDTO):
    result = await AuthService.login(dto)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": result}

@router.post("/verify-email")
async def verify_email_code(dto: VerifyEmailDTO):
    is_valid = await AuthService.verify_email_code(dto.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Token de verificação inválido ou expirado")

    return {"message": "E-mail verificado com sucesso"}

@router.post("/send-code-verify-email")
async def send_code_verify_email(dto: SendVerifyEmailCodeDTO):
    sent = await AuthService.send_code_verify_email(dto.email)
    if not sent:
        raise HTTPException(status_code=400, detail="Não foi possível enviar o código de verificação de e-mail")

    return {"message": "Código de verificação de e-mail enviado com sucesso"}
    
@router.post("/logout")
async def logout():
    await AuthService.logout()
    return {"message": "Logout realizado com sucesso"}
