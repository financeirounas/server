from typing import List, Optional
from fastapi import HTTPException
from lib.supabase_client import supabase
from entities.models.unit import Unit

class UnitRepository:
    TABLE_NAME = "units"

    @staticmethod
    async def list_units(unit_type: Optional[str] = None) -> List[Unit]:
        query = supabase.table(UnitRepository.TABLE_NAME).select("*")
        if unit_type:
            query = query.eq("type", unit_type)
        response = query.execute()
        if not response.data:
            return []
        return [Unit(**item) for item in response.data]

    @staticmethod
    async def get_unit_by_id(unit_id: str) -> Optional[Unit]:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .select("*")
            .eq("id", unit_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Unit(**response.data[0])

    @staticmethod
    async def create_unit(data: dict) -> Unit:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .insert(data)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Erro ao criar unidade no Supabase")
        return Unit(**response.data[0])

    @staticmethod
    async def update_unit(unit_id: str, data: dict) -> Unit:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .update(data)
            .eq("id", unit_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Erro ao atualizar unidade no Supabase")
        return Unit(**response.data[0])

    @staticmethod
    async def delete_unit(unit_id: str) -> None:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .delete()
            .eq("id", unit_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Erro ao deletar unidade no Supabase")
        return None
        
    @staticmethod
    async def get_unit_by_name(name: str) -> Optional[Unit]:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .select("*")
            .eq("name", name)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Unit(**response.data[0])

    @staticmethod
    async def get_unit_by_address(address: str) -> Optional[Unit]:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .select("*")
            .eq("address", address)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Unit(**response.data[0])

    @staticmethod
    async def get_unit_by_type(type: str) -> List[Unit]:
        response = (
            supabase.table(UnitRepository.TABLE_NAME)
            .select("*")
            .eq("type", type)
            .execute()
        )
        if not response.data:
            return []
        return [Unit(**item) for item in response.data]

    