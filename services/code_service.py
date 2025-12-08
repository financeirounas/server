import random
import uuid

from fastapi import HTTPException

from entities.models.security_code import SecurityCode
from repositories.code_repository import CodeRepository



class CodeService:

    @staticmethod
    async def generate_security_code(user_id: str, code_type: str) -> str:    
        if code_type == "reset_password":
            return ''.join([str(random.randint(0, 9)) for _ in range(6)])
        elif code_type == "email_verification":
            return f"UNAS_{uuid.uuid4()}"
        elif code_type == "reset_password_token":
            return str(uuid.uuid4())
        else:
            raise HTTPException(status_code=400, detail="Tipo de código de segurança inválido.")
        
        
    @staticmethod
    async def create_security_code(user_id: str, code_type: str) -> SecurityCode:
        code = await CodeService.generate_security_code(user_id, code_type)            
        record = await CodeRepository.create_security_code(
            user_id=user_id,
            type=code_type,
            code=code
        )
        return record
    
    
    @staticmethod
    async def get_security_code_by_code(code: str) -> SecurityCode | None:
        record = await CodeRepository.get_security_code("code", code)
        if record:
            return record
        return None
    
        
    
    
    
        
        
        