from typing import List, Optional
from fastapi import HTTPException
from repositories.unit_user_repository import UnitUserRepository
from repositories.user_repository import UserRepository
from repositories.unit_repository import UnitRepository
from entities.dtos.unit_user_dto import UnitUserCreateDTO, UnitUserResponseDTO, UnitUserUpdateDTO
from entities.dtos.unit_dto import UnitResponseDTO
from entities.dtos.user_dto import UserResponseDTO
from zoneinfo import ZoneInfo

def to_brazil(dt):
    if dt is None:
        return None
    return dt.astimezone(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

class UnitUserService:

    @staticmethod
    async def create_unit_user(dto: UnitUserCreateDTO) -> UnitUserResponseDTO:
        # Valida existência de user e unit
        user = await UserRepository.get_user("id", dto.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        unit = await UnitRepository.get_unit_by_id(dto.unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        # Verifica duplicata (mesmo user_id + unit_id)
        existing_list = await UnitUserRepository.list_unit_users_by_user(dto.user_id)
        for ex in existing_list:
            if ex.unit_id == dto.unit_id:
                raise HTTPException(status_code=400, detail="Associação usuário-unidade já existe")

        unit_user = await UnitUserRepository.create_unit_user(dto.unit_id, dto.user_id, dto.role)
        return UnitUserResponseDTO(
            id=unit_user.id,
            unit_id=unit_user.unit_id,
            user_id=unit_user.user_id,
            role=unit_user.role,
            created_at=to_brazil(unit_user.created_at),
            updated_at=to_brazil(unit_user.updated_at),
        )

    @staticmethod
    async def list_all_unit_users() -> List[UnitUserResponseDTO]:
        unit_users = await UnitUserRepository.list_all_unit_users()
        return [
            UnitUserResponseDTO(
                id=unit_user.id,
                unit_id=unit_user.unit_id,
                user_id=unit_user.user_id,
                role=unit_user.role,
                created_at=to_brazil(unit_user.created_at),
                updated_at=to_brazil(unit_user.updated_at),
            ) for unit_user in unit_users
        ]

    @staticmethod
    async def update_unit_user(unit_user_id: str, dto: UnitUserUpdateDTO) -> UnitUserResponseDTO:
        # Apenas role é atualizável atualmente
        unit_user = await UnitUserRepository.update_unit_user(unit_user_id, dto.role)
        if not unit_user:
            raise HTTPException(status_code=404, detail="Associação não encontrada")

        return UnitUserResponseDTO(
            id=unit_user.id,
            unit_id=unit_user.unit_id,
            user_id=unit_user.user_id,
            role=unit_user.role,
            created_at=to_brazil(unit_user.created_at),
            updated_at=to_brazil(unit_user.updated_at),
        )

    @staticmethod
    async def get_unit_user_by_id(unit_user_id: str) -> UnitUserResponseDTO:
        unit_user = await UnitUserRepository.get_unit_user_by_id(unit_user_id)
        if not unit_user:
            raise HTTPException(status_code=404, detail="Associação não encontrada")

        return UnitUserResponseDTO(
            id=unit_user.id,
            unit_id=unit_user.unit_id,
            user_id=unit_user.user_id,
            role=unit_user.role,
            created_at=to_brazil(unit_user.created_at),
            updated_at=to_brazil(unit_user.updated_at),
        )

    @staticmethod
    async def list_users_by_unit(unit_id: str) -> List[UserResponseDTO]:
        "Lista todos os usuários associados a uma dada unidade."
        unit = await UnitRepository.get_unit_by_id(unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")
        users = await UnitUserRepository.list_users_by_unit(unit_id)
        return [
            UserResponseDTO(
                id=user.id,
                username=getattr(user, "username", None) or getattr(user, "name", None),
                email=user.email,
                role=getattr(user, "role", None),
                units=None,
            ) for user in users
        ]
        

    @staticmethod
    async def list_unit_by_user(user_id: str) -> List[UnitResponseDTO]:
        "Lista todas as unidades para um dado usuário."
        unit = await UserRepository.get_user("id", user_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        units = await UnitUserRepository.list_units_by_user(user_id)
        return [
            UnitResponseDTO(
                id=unit.id,
                name=unit.name,
                address=unit.address if hasattr(unit, "address") else None,
                type=unit.type if hasattr(unit, "type") else None,
                capacity=unit.capacity if hasattr(unit, "capacity") else None,
                created_at=to_brazil(unit.created_at),
                updated_at=to_brazil(unit.updated_at),
            ) for unit in units
        ]

    @staticmethod
    async def delete_unit_user(unit_user_id: str) -> None:
        await UnitUserRepository.delete_unit_user(unit_user_id)