from zoneinfo import ZoneInfo
from fastapi import HTTPException
from lib.supabase_client import supabase  
from entities.models.unit_user import UnitUser
from repositories.user_repository import UserRepository
from repositories.unit_repository import UnitRepository
from entities.models.user import User
from entities.models.unit import Unit
from datetime import datetime

class UnitUserRepository:

    TABLE_NAME = "unit_users"

    @staticmethod
    async def create_unit_user(
        unit_id: str,
        user_id: str,
        role: str,
    ) -> UnitUser | None:
        """
        Cria a relação unidade-usuário na tabela 'unit_users' do Supabase.
        Retorna o registro criado como dict.
        """

        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .insert(
                {
                    "unit_id": unit_id,
                    "user_id": user_id,
                    "role": role,
                }
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar relação unidade-usuário no Supabase")

        return UnitUser(**response.data[0])
    
    @staticmethod
    async def get_unit_user(key: str, value: str) -> UnitUser | None:
        """
        Busca uma relação unidade-usuário pelo campo especificado.
        Retorna dict ou None.
        """
        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .select("*")
            .eq(key, value)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return UnitUser(**response.data[0])
    
    @staticmethod
    async def update_unit_user(unit_user_id: str, role: str | None = None) -> UnitUser | None:
        """
        Atualiza campos permitidos da relação unidade-usuário e retorna o registro atualizado.
        """
        payload: dict = {}
        if role is not None:
            payload["role"] = role
            payload["updated_at"] = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()

        if not payload:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .update(payload)
            .eq("id", unit_user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar relação unidade-usuário no Supabase")

        try:
            return UnitUser(**response.data[0])
        except Exception:
            return None
        
    @staticmethod
    async def delete_unit_user(unit_user_id: str) -> None:
        """
        Deleta a relação unidade-usuário pelo ID.
        """
        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .delete()
            .eq("id", unit_user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao deletar relação unidade-usuário no Supabase")
        
    @staticmethod
    async def list_unit_users_by_unit(unit_id: str) -> list[UnitUser]:
        """
        Lista todas as relações unidade-usuário para uma unidade específica.
        """
        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .select("*")
            .eq("unit_id", unit_id)
            .execute()
        )

        if not response.data:
            return []

        unit_users = []
        for item in response.data:
            try:
                unit_users.append(UnitUser(**item))
            except Exception:
                # Ignora registros que não batem com o modelo UnitUser
                continue

        return unit_users
    
    @staticmethod
    async def list_unit_users_by_user(user_id: str) -> list[UnitUser]:
        """
        Lista todas as relações unidade-usuário para um usuário específico.
        """
        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            return []

        unit_users = []
        for item in response.data:
            try:
                unit_users.append(UnitUser(**item))
            except Exception:
                # Ignora registros que não batem com o modelo UnitUser
                continue

        return unit_users
    
    @staticmethod
    async def list_all_unit_users() -> list[UnitUser]:
        """
        Lista todas as relações unidade-usuário.
        """
        response = (
            supabase.table(UnitUserRepository.TABLE_NAME)
            .select("*")
            .execute()
        )

        if not response.data:
            return []

        unit_users = []
        for item in response.data:
            try:
                unit_users.append(UnitUser(**item))
            except Exception:
                # Ignora registros que não batem com o modelo UnitUser
                continue

        return unit_users
    
    @staticmethod
    async def get_unit_user_by_id(unit_user_id: str) -> UnitUser | None:
        """
        Retorna a relação unidade-usuário pelo ID.
        """
        return await UnitUserRepository.get_unit_user("id", unit_user_id)

    @staticmethod
    async def list_users_by_unit(unit_id: str) -> list[User]:
        """Retorna lista de Users associados a uma unidade."""
        unit_users = await UnitUserRepository.list_unit_users_by_unit(unit_id)
        users: list[User] = []
        for uu in unit_users:
            user = await UserRepository.get_user("id", uu.user_id)
            if user:
                users.append(user)
        return users

    @staticmethod
    async def list_units_by_user(user_id: str) -> list[Unit]:
        """Retorna lista de Units associados a um usuário."""
        unit_users = await UnitUserRepository.list_unit_users_by_user(user_id)
        units: list[Unit] = []
        for uu in unit_users:
            unit = await UnitRepository.get_unit_by_id(uu.unit_id)
            if unit:
                units.append(unit)
        return units