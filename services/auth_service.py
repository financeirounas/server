import os
from entities.dtos.auth_dto import LoginDTO
from repositories.code_repository import CodeRepository
from repositories.user_repository import UserRepository
from services.code_service import CodeService
from services.code_service import CodeService
from services.email_service import EmailService
from services.user_service import UserService

class AuthService:
    
    """
    Função para inicializar o usuário administrador padrão.
    """
    @staticmethod
    async def initialize_admin_user():
        admin_email = os.getenv("ADMIN_USER_EMAIL", "admin@unas.org.br")
        admin_password = os.getenv("ADMIN_USER_PASSWORD", "123456")
        admin_username = os.getenv("ADMIN_USERNAME", "adminunas")
        type = "admin"

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
            type=type
        )
        
        
        code = await CodeService.create_security_code(user.id, "email_verification")
        await EmailService.send_email_verification(user.email, user.username, code.code)
        
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

    """
    Função para login de usuário.
    """
    @staticmethod
    async def login(dto: LoginDTO):
        if dto.email == "admin@unas.org.br" and dto.password == "123456":
            return "fake-token-123"

        return None
    
    
    
    @staticmethod
    async def logout():
        pass

    @staticmethod
    async def reset_password(email: str):
        pass

    @staticmethod
    async def verify_token(code: str):
        pass

    @staticmethod
    async def change_password(user_id: int, new_password: str):
        pass
