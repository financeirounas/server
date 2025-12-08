import os
from fastapi import HTTPException
from entities.models.user import User
from repositories.code_repository import CodeRepository
from repositories.unit_repository import UnitRepository
from repositories.user_repository import UserRepository
from services.code_service import CodeService
from services.code_service import CodeService
from services.email_service import EmailService
from services.jwt_service import JWTService
from services.user_service import UserService
from repositories.unit_user_repository import UnitUserRepository

class AuthService:
    
    """
    Função para inicializar o usuário administrador padrão.
    """
    @staticmethod
    async def initialize_admin_user():
        admin_email = os.getenv("ADMIN_USER_EMAIL", "admin@unas.org.br")
        admin_password = os.getenv("ADMIN_USER_PASSWORD", "123456")
        admin_username = os.getenv("ADMIN_USERNAME", "adminunas")
        role = "gestor"

        print(
            f"[INIT] Tentando inicializar admin: "
            f"email={admin_email}, username={admin_username}"
        )

        existing = await UserRepository.get_user("email", admin_email)
        if existing:
            print("[INIT] Admin já existe. Nada a fazer.")
            return None

        user = await UserService.register_user(
            email=admin_email,
            password=admin_password,
            username=admin_username,
            role=role
        )
        
        
        code = await CodeService.create_security_code(user.id, "email_verification")
        await EmailService.send_email_verification(user.email, user.username, code.code)
        
        unit = await UnitRepository.create_unit({
            "name": "Unidade Administrativa - Teste",
            "type": "CCA",
            "address": "Endereço Administrativo",
            "capacity": 100,
        })
        
        if not unit:
            raise HTTPException(status_code=500, detail="Erro ao criar unidade administrativa para o usuário admin.")
        
        
        await UnitUserRepository.create_unit_user(
            unit.id,
            user.id,
            "gestor"
        )

        print("[INIT] Usuário admin criado com sucesso.")
        return None
    
    
    """
    Função para verificação de token de e-mail.
    
    """
    @staticmethod
    async def verify_email_code(code: str) -> bool:
        code_record = await CodeService.get_security_code_by_code(code)
        
        if not code_record or not code_record.type == "email_verification" or code_record.revoked:
            return False

        user_record = await UserRepository.get_user("id", code_record.user_id)
        if user_record:
            await UserRepository.update_user_email_verified(user_record.id, True)
            await CodeRepository.mark_code_as_revoked(code_record.id)
            return True
        
        
    @staticmethod
    async def verify_reset_password_code(code: str) -> User | None:
        
        code_record = await CodeService.get_security_code_by_code(code)
        
        if not code_record or not (code_record.type == "reset_password" or code_record.type == "reset_password_token") or code_record.revoked:
            return False

        user_record = await UserRepository.get_user("id", code_record.user_id)
        if user_record:
            await CodeRepository.mark_code_as_revoked(code_record.id)
            return user_record


    @staticmethod
    async def send_code_verify_email(email: str) -> bool:
        user_record = await UserRepository.get_user("email", email)
        
        if not user_record:
            return False
        
        await CodeRepository.revoke_all_codes_for_user(user_record.id, "email_verification")
        code = await CodeService.create_security_code(user_record.id, "email_verification")
        
        if not code:
            return False
        
        await EmailService.send_email_verification(user_record.email, user_record.username, code.code) 
        return True
    
    
    @staticmethod
    async def send_reset_password_code(email: str) -> bool:
        user_record = await UserRepository.get_user("email", email)
        
        if not user_record:
            return False
        
        await CodeRepository.revoke_all_codes_for_user(user_record.id, "reset_password")
        code = await CodeService.create_security_code(user_record.id, "reset_password")
        
        if not code:
            return False
        
        await EmailService.send_email_reset_password(user_record.email, user_record.username, code.code) 
        return True

    """
    Função para login de usuário.
    """
    @staticmethod
    async def login(email, password) -> dict:
        
        user_record = await UserRepository.get_user("email", email)
        
        print(user_record)
        if not user_record:
            raise HTTPException(status_code=400, detail="Invalid email or password.")
        
        if not UserService.verify_password(password, user_record.password):
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        generated_jwt = await JWTService.generate_jwt_token(user_record.id)
        if not generated_jwt:
            raise RuntimeError("Erro ao gerar token JWT.")
        
                
        return {
            "access_token": generated_jwt,
            "user": {
                "id": user_record.id,
                "email": user_record.email,
                "username": user_record.username,
                "role": user_record.role,
                "email_verified": user_record.email_verified
            },
        }
    
    
    @staticmethod
    async def change_password(user_id: int, new_password: str):
        hashed_password = UserService.hash_password(new_password)
        await UserRepository.update_user_password(user_id, hashed_password)