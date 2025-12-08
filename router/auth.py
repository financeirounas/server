from fastapi import APIRouter, HTTPException
from services.auth_service import AuthService
from entities.dtos.auth_dto import LoginDTO, ResetPasswordCodeDTO, SendVerifyEmailCodeDTO, ValidateTokenDTO, VerifyEmailDTO
from services.code_service import CodeService
from services.jwt_service import JWTService

router = APIRouter()

@router.post("/login")
async def login(dto: LoginDTO):
    result = await AuthService.login(dto.email, dto.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return result

@router.post("/send-code")
async def send_code(dto: SendVerifyEmailCodeDTO):
    await AuthService.send_reset_password_code(dto.email)
    return {"message": "Código de redefinição de senha enviado com sucesso"}

@router.post("/validate-code")
async def validate_code(dto: VerifyEmailDTO):
    user_record = await AuthService.verify_reset_password_code(dto.code)
    if not user_record:
        raise HTTPException(status_code=400, detail="Token de verificação inválido ou expirado")
    
    security_code = await CodeService.create_security_code(user_record.id, "reset_password_token")
    return {"message": "E-mail verificado com sucesso", "reset_password_token": security_code.code}

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
  
  
@router.post("/reset-password")
async def reset_password_code(dto: ResetPasswordCodeDTO):
    user_record = await AuthService.verify_reset_password_code(dto.token)
    if not user_record:
        raise HTTPException(status_code=400, detail="Token de redefinição de senha inválido ou expirado")
    
    if dto.password != dto.confirm:
        raise HTTPException(status_code=400, detail="A senha e a confirmação de senha não coincidem")
    
    await AuthService.change_password(user_record.id, dto.password)
    return {"message": "Senha redefinida com sucesso"}

 
@router.post("/validate-token")
async def validate_token(dto: ValidateTokenDTO):
    payload = await JWTService.validate_token(dto.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return {"payload": payload}  

@router.post("/logout")
async def logout():
    await AuthService.logout()
    return {"message": "Logout realizado com sucesso"}
