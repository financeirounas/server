from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.storage_service import StorageService
from entities.dtos.storage_dto import StorageEntryDTO, StorageExitDTO, StorageResponseDTO

router = APIRouter()

@router.get("", response_model=List[StorageResponseDTO])
async def get_storage(unit_id: str = Query(..., description="ID da unidade")):
    """
    Lista todos os itens de estoque de uma unidade.
    """
    try:
        return await StorageService.get_storage_by_unit(unit_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estoque: {str(e)}")

@router.post("/entry", response_model=StorageResponseDTO)
async def register_entry(dto: StorageEntryDTO):
    """
    Registra entrada de estoque.
    Se o item já existe, incrementa a quantidade (initial_quantity).
    Caso contrário, cria um novo registro.
    """
    try:
        return await StorageService.register_entry(dto)
    except HTTPException as e:
        # Propaga HTTPExceptions com suas mensagens originais
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar entrada: {str(e)}")

@router.post("/exit", response_model=List[StorageResponseDTO])
async def register_exit(dto: StorageExitDTO):
    """
    Registra saída de estoque.
    Valida disponibilidade antes de decrementar (incrementa used_quantity).
    """
    try:
        return await StorageService.register_exit(dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar saída: {str(e)}")
