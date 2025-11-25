from typing import Optional, Dict, Any

from fastapi import HTTPException
from lib.supabase_client import supabase  
from entities.models.security_code import SecurityCode

class CodeRepository:

    TABLE_NAME = "security_codes"

    @staticmethod
    async def create_security_code(
        user_id: str,
        type: str,
        code: str
    ) -> SecurityCode:
        """
        Cria o codigo de segurança  na tabela 'security_codes' do Supabase.
        Retorna o registro criado como dict.
        """

        response = (
            supabase.table(CodeRepository.TABLE_NAME)
            .insert(
                {
                    "user_id": user_id,
                    "type": type,
                    "code": code,
                    "revoked": False
                }
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar codigo de segurança no Supabase")
        
        return SecurityCode(**response.data[0])

    @staticmethod
    async def get_security_code(key: str, value: str) -> SecurityCode | None:
        """
        Busca um código de segurança pelo campo especificado.
        Retorna dict ou None.
        """
        response = (
            supabase.table(CodeRepository.TABLE_NAME)
            .select("*")
            .eq(key, value)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return SecurityCode(**response.data[0])
    
    @staticmethod
    async def mark_code_as_revoked(code_id: str) -> None:
        """
        Marca um código de segurança como revogado.
        """
        response = (
            supabase.table(CodeRepository.TABLE_NAME)
            .update({"revoked": True})
            .eq("id", code_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao revogar o código de segurança no Supabase")
    

    @staticmethod
    async def revoke_all_codes_for_user(user_id: str, code_type: str) -> None:
        """
        Revoga todos os códigos de um determinado tipo para um usuário.
        """
        response = (
            supabase.table(CodeRepository.TABLE_NAME)
            .update({"revoked": True})
            .eq("user_id", user_id)
            .eq("type", code_type)
            .execute()
        )
    