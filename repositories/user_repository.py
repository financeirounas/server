from typing import Optional, Dict, Any

from fastapi import HTTPException
from lib.supabase_client import supabase  
from entities.models.user import User

class UserRepository:

    TABLE_NAME = "users"

    @staticmethod
    async def create_user(
        email: str,
        hashed_password: str,
        username: str,
        role: str,
    ) -> User | None:
        """
        Cria o usuário na tabela 'users' do Supabase.
        Retorna o registro criado como dict.
        """

        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .insert(
                {
                    "email": email,
                    "password": hashed_password,
                    "username": username,
                    "role": role,
                    "email_verified": False
                }
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário no Supabase")
        
        return User(**response.data[0])

    @staticmethod
    async def get_user(key: str, value: str) -> User | None:
        """
        Busca um usuário pelo email.
        Retorna dict ou None.
        """
        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .select("*")
            .eq(key, value)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return User(**response.data[0])
    
    @staticmethod
    async def update_user_email_verified(user_id: str, email_verified: bool) -> None:
        """
        Atualiza o campo email_verified do usuário.
        """
        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .update({"email_verified": email_verified})
            .eq("id", user_id)
            .execute()
        )
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar email_verified do usuário no Supabase")
        
        
    @staticmethod
    async def update_user_password(user_id: str, hashed_password: str) -> None:
        """
        Atualiza a senha do usuário.
        """
        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .update({"password": hashed_password})
            .eq("id", user_id)
            .execute()
        )
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar a senha do usuário no Supabase")    
        

    @staticmethod
    async def delete_user(user_id: str) -> None:
        """
        Deleta o usuário pelo ID.
        """
        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .delete()
            .eq("id", user_id)
            .execute()
        )
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao deletar o usuário no Supabase")