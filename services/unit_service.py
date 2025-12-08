from typing import List, Optional
from fastapi import HTTPException
from repositories.unit_repository import UnitRepository
from entities.dtos.unit_dto import (
    UnitCreateDTO,
    UnitUpdateDTO,
    UnitResponseDTO,
)


class UnitService:

    @staticmethod
    async def list_units(unit_type: Optional[str] = None) -> List[UnitResponseDTO]:
        units = await UnitRepository.list_units(unit_type)
        return [
            UnitResponseDTO(
                id=unit.id,
                name=unit.name,
                address=unit.address,
                type=unit.type,
                capacity=unit.capacity,
                created_at=unit.created_at.isoformat() if unit.created_at else None,
                updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
            )
            for unit in units
        ]

    @staticmethod
    async def get_unit_by_id(unit_id: str) -> UnitResponseDTO:
        unit = await UnitRepository.get_unit_by_id(unit_id)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        return UnitResponseDTO(
            id=unit.id,
            name=unit.name,
            address=unit.address,
            type=unit.type,
            capacity=unit.capacity,
            created_at=unit.created_at.isoformat() if unit.created_at else None,
            updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
        )

    @staticmethod
    async def create_unit(dto: UnitCreateDTO) -> UnitResponseDTO:
        unit = await UnitRepository.create_unit(dto.model_dump())
        return UnitResponseDTO(
            id=unit.id,
            name=unit.name,
            address=unit.address,
            type=unit.type,
            capacity=unit.capacity,
            created_at=unit.created_at.isoformat() if unit.created_at else None,
            updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
        )

    @staticmethod
    async def update_unit(unit_id: str, dto: UnitUpdateDTO) -> UnitResponseDTO:
        # exclude_unset=True para não sobrescrever com None campos não enviados
        data = dto.model_dump(exclude_unset=True)
        unit = await UnitRepository.update_unit(unit_id, data)

        return UnitResponseDTO(
            id=unit.id,
            name=unit.name,
            address=unit.address,
            type=unit.type,
            capacity=unit.capacity,
            created_at=unit.created_at.isoformat() if unit.created_at else None,
            updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
        )

    @staticmethod
    async def delete_unit(unit_id: str) -> None:
        await UnitRepository.delete_unit(unit_id)

    @staticmethod
    async def get_unit_by_name(name: str) -> UnitResponseDTO:
        unit = await UnitRepository.get_unit_by_name(name)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        return UnitResponseDTO(
            id=unit.id,
            name=unit.name,
            address=unit.address,
            type=unit.type,
            capacity=unit.capacity,
            created_at=unit.created_at.isoformat() if unit.created_at else None,
            updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
        )

    @staticmethod
    async def get_unit_by_address(address: str) -> UnitResponseDTO:
        unit = await UnitRepository.get_unit_by_address(address)
        if not unit:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")

        return UnitResponseDTO(
            id=unit.id,
            name=unit.name,
            address=unit.address,
            type=unit.type,
            capacity=unit.capacity,
            created_at=unit.created_at.isoformat() if unit.created_at else None,
            updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
        )

    @staticmethod
    async def get_unit_by_type(type: str) -> List[UnitResponseDTO]:
        units = await UnitRepository.get_unit_by_type(type)
        return [
            UnitResponseDTO(
                id=unit.id,
                name=unit.name,
                address=unit.address,
                type=unit.type,
                created_at=unit.created_at.isoformat() if unit.created_at else None,
                updated_at=unit.updated_at.isoformat() if unit.updated_at else None,
            )
            for unit in units
        ]