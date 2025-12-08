from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path
from entities.dtos.unit_dto import (
    UnitCreateDTO,
    UnitUpdateDTO,
    UnitResponseDTO,
)
from services.unit_service import UnitService

router = APIRouter()


@router.get("", response_model=List[UnitResponseDTO])
async def list_units(
    type: Optional[str] = Query(
        None,
        description="Filtra por tipo de unidade (ex: CCA, CEI)",
    )
):
    """
    Lista todas as unidades, com filtro opcional por tipo.
    """
    try:
        return await UnitService.list_units(type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar unidades: {str(e)}",
        )


@router.get("/{unit_id}", response_model=UnitResponseDTO)
async def get_unit(
    unit_id: str = Path(..., description="ID da unidade"),
):
    """
    Busca uma unidade pelo ID.
    """
    try:
        return await UnitService.get_unit_by_id(unit_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar unidade: {str(e)}",
        )


@router.post("", response_model=UnitResponseDTO, status_code=201)
async def create_unit(dto: UnitCreateDTO):
    """
    Cria uma nova unidade.
    """
    try:
        return await UnitService.create_unit(dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar unidade: {str(e)}",
        )


@router.put("/{unit_id}", response_model=UnitResponseDTO)
async def update_unit(
    unit_id: str = Path(..., description="ID da unidade"),
    dto: UnitUpdateDTO = ...,
):
    """
    Atualiza os dados de uma unidade.
    """
    try:
        return await UnitService.update_unit(unit_id, dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar unidade: {str(e)}",
        )


@router.delete("/{unit_id}", status_code=204)
async def delete_unit(
    unit_id: str = Path(..., description="ID da unidade"),
):
    """
    Remove uma unidade.
    """
    try:
        await UnitService.delete_unit(unit_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar unidade: {str(e)}",
        )

@router.get("/name/{name}", response_model=UnitResponseDTO)
async def get_unit_by_name(name: str = Path(..., description="Nome da unidade")):
    """
    Busca uma unidade pelo nome.
    """
    try:
        return await UnitService.get_unit_by_name(name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar unidade por nome: {str(e)}",
        )

@router.get("/address/{address}", response_model=UnitResponseDTO)
async def get_unit_by_address(address: str = Path(..., description="Endereço da unidade")):
    """
    Busca uma unidade pelo endereço.
    """
    try:
        return await UnitService.get_unit_by_address(address)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar unidade por endereço: {str(e)}",
        )

@router.get("/type/{type}", response_model=List[UnitResponseDTO])
async def get_unit_by_type(type: str = Path(..., description="Tipo da unidade")):
    """
    Busca todas as unidades de um tipo.
    """
    try:
        return await UnitService.get_unit_by_type(type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar unidade por tipo: {str(e)}",
        )