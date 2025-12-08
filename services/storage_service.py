from typing import List
from fastapi import HTTPException
from repositories.storage_repository import StorageRepository
from entities.models.storage import Storage
from entities.dtos.storage_dto import (
    StorageEntryDTO,
    StorageExitDTO,
    StorageResponseDTO,
)
from datetime import datetime


class StorageService:

    @staticmethod
    async def get_storage_by_unit(unit_id: str) -> List[StorageResponseDTO]:
        """
        Lista todos os itens de estoque de uma unidade.
        Retorna lista de StorageResponseDTO.
        """
        storage_items = await StorageRepository.get_storage_by_unit(unit_id)

        return [
            StorageResponseDTO(
                id=item.id,
                name=item.name,
                amount=item.amount,
                unit_id=item.unit_id,
                type=item.type,
                initial_quantity=item.initial_quantity,
                used_quantity=item.used_quantity,
                current_quantity=(item.initial_quantity - item.used_quantity),
                created_at=item.created_at.isoformat() if item.created_at else None,
                updated_at=item.updated_at.isoformat() if item.updated_at else None,
            )
            for item in storage_items
        ]

    @staticmethod
    async def register_entry(dto: StorageEntryDTO) -> StorageResponseDTO:
        """
        Registra entrada de estoque.
        Se o item já existe (mesmo name + unit_id), incrementa initial_quantity.
        Caso contrário, cria um novo registro.
        Retorna o item atualizado ou criado.
        """
        # Valida o tipo de entrada (opcional, mantive a validação)
        if dto.type not in ["comprado", "doado"]:
            raise HTTPException(
                status_code=400,
                detail="Tipo de entrada deve ser 'comprado' ou 'doado'",
            )

        try:
            existing = await StorageRepository.get_storage_item(dto.unit_id, dto.name)
            if existing:
                # Incrementa initial_quantity; também atualiza preço (amount) e type se vierem no DTO
                updated = await StorageRepository.increment_initial_quantity(
                    storage_id=existing.id,
                    increment=dto.initial_quantity,
                    new_amount=dto.amount,
                    new_type=dto.type,
                )

                return StorageResponseDTO(
                    id=updated.id,
                    name=updated.name,
                    amount=updated.amount,
                    unit_id=updated.unit_id,
                    type=updated.type,
                    initial_quantity=updated.initial_quantity,
                    used_quantity=updated.used_quantity,
                    current_quantity=(updated.initial_quantity - updated.used_quantity),
                    created_at=updated.created_at.isoformat() if updated.created_at else None,
                    updated_at=updated.updated_at.isoformat() if updated.updated_at else None,
                )
            else:
                # Cria novo item
                created = await StorageRepository.create_storage_item(
                    unit_id=dto.unit_id,
                    name=dto.name,
                    amount=dto.amount,
                    type=dto.type,
                    initial_quantity=dto.initial_quantity,
                )
                return StorageResponseDTO(
                    id=created.id,
                    name=created.name,
                    amount=created.amount,
                    unit_id=created.unit_id,
                    type=created.type,
                    initial_quantity=created.initial_quantity,
                    used_quantity=created.used_quantity,
                    current_quantity=(created.initial_quantity - created.used_quantity),
                    created_at=created.created_at.isoformat() if created.created_at else None,
                    updated_at=created.updated_at.isoformat() if created.updated_at else None,
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao registrar entrada: {str(e)}")

    @staticmethod
    async def register_exit(dto: StorageExitDTO) -> List[StorageResponseDTO]:
        """
        Registra saída de estoque.
        Para cada item na lista, incrementa used_quantity (consumo).
        Valida disponibilidade antes de cada incremento.
        """
        updated_items: List[StorageResponseDTO] = []

        for item in dto.items:
            try:
                existing = await StorageRepository.get_storage_item(dto.unit_id, item.name)
                if not existing:
                    raise HTTPException(status_code=404, detail=f"Item '{item.name}' não encontrado")

                # calcular novo used_quantity (incremental)
                new_used_quantity = existing.used_quantity + item.used_quantity

                # valida e aplica
                updated = await StorageRepository.update_storage_used_quantity(
                    storage_id=existing.id,
                    new_used_quantity=new_used_quantity,
                )

                updated_items.append(
                    StorageResponseDTO(
                        id=updated.id,
                        name=updated.name,
                        amount=updated.amount,
                        unit_id=updated.unit_id,
                        type=updated.type,
                        initial_quantity=updated.initial_quantity,
                        used_quantity=updated.used_quantity,
                        current_quantity=(updated.initial_quantity - updated.used_quantity),
                        created_at=updated.created_at.isoformat() if updated.created_at else None,
                        updated_at=updated.updated_at.isoformat() if updated.updated_at else None,
                    )
                )
            except HTTPException as e:
                # Propaga o erro com contexto do item
                raise HTTPException(
                    status_code=e.status_code,
                    detail=f"Erro ao processar item '{item.name}': {e.detail}",
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro inesperado ao processar item '{item.name}': {str(e)}",
                )

        return updated_items

    @staticmethod
    async def get_item_by_name_and_unit(unit_id: str, name: str) -> StorageResponseDTO:
        """
        Busca um item de estoque específico por nome e unidade.
        Retorna StorageResponseDTO.
        """
        item = await StorageRepository.get_storage_item(unit_id, name)
        if not item:
            raise HTTPException(status_code=404, detail="Item de estoque não encontrado")

        return StorageResponseDTO(
            id=item.id,
            name=item.name,
            amount=item.amount,
            unit_id=item.unit_id,
            type=item.type,
            initial_quantity=item.initial_quantity,
            used_quantity=item.used_quantity,
            current_quantity=(item.initial_quantity - item.used_quantity),
            created_at=item.created_at.isoformat() if item.created_at else None,
            updated_at=item.updated_at.isoformat() if item.updated_at else None,
        )

    @staticmethod
    async def add_new_item(
        unit_id: str,
        name: str,
        amount: float,
        type: str,
        initial_quantity: int,
    ) -> StorageResponseDTO:
        """
        Adiciona um novo item ao estoque.
        Retorna o item criado.
        """
        try:
            item = await StorageRepository.create_storage_item(
                unit_id=unit_id,
                name=name,
                amount=amount,
                type=type,
                initial_quantity=initial_quantity,
            )
            return StorageResponseDTO(
                id=item.id,
                name=item.name,
                amount=item.amount,
                unit_id=item.unit_id,
                type=item.type,
                initial_quantity=item.initial_quantity,
                used_quantity=item.used_quantity,
                current_quantity=(item.initial_quantity - item.used_quantity),
                created_at=item.created_at.isoformat() if item.created_at else None,
                updated_at=item.updated_at.isoformat() if item.updated_at else None,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro ao adicionar item ao estoque: {str(e)}"
            )

    @staticmethod
    async def update_used_quantity(unit_id: str, name: str, used_quantity: int) -> StorageResponseDTO:
        """
        Atualiza a quantidade utilizada de um item no estoque para um valor absoluto.
        Retorna o item atualizado.
        """
        try:
            existing_item = await StorageRepository.get_storage_item(unit_id, name)
            if not existing_item:
                raise HTTPException(status_code=404, detail="Item de estoque não encontrado")

            # valida e aplica
            updated_item = await StorageRepository.update_storage_used_quantity(
                storage_id=existing_item.id,
                new_used_quantity=used_quantity,
            )

            return StorageResponseDTO(
                id=updated_item.id,
                name=updated_item.name,
                amount=updated_item.amount,
                unit_id=updated_item.unit_id,
                type=updated_item.type,
                initial_quantity=updated_item.initial_quantity,
                used_quantity=updated_item.used_quantity,
                current_quantity=(updated_item.initial_quantity - updated_item.used_quantity),
                created_at=updated_item.created_at.isoformat() if updated_item.created_at else None,
                updated_at=updated_item.updated_at.isoformat() if updated_item.updated_at else None,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro ao atualizar quantidade utilizada: {str(e)}"
            )
