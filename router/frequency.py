from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path
from services.frequency_service import FrequencyService
from entities.dtos.frequency_dto import FrequencyResponseDTO, FrequencyCreateDTO, FrequencyUpdateDTO

router = APIRouter()

@router.get("", response_model=List[FrequencyResponseDTO])
async def list_frequencies(
    initial_date: Optional[str] = Query(None, description="Data inicial para filtro (YYYY-MM-DD)"),
    final_date: Optional[str] = Query(None, description="Data final para filtro (YYYY-MM-DD)"),
    unit_id: Optional[str] = Query(None, description="ID da unidade para filtro"),
):
    """
    Lista todas as frequências, com filtros opcionais por período e unidade.
    """
    try:
        frequencies = await FrequencyService.list_frequencies(
            initial_date=initial_date,
            final_date=final_date,
            unit_id=unit_id,
        )
        return frequencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar frequências: {str(e)}")
    
@router.get("/{frequency_id}", response_model=FrequencyResponseDTO)
async def get_frequency_by_id(
    frequency_id: str = Path(..., description="ID da frequência a ser buscada")
):
    """
    Busca uma frequência pelo ID.
    """
    try:
        frequency = await FrequencyService.get_frequency_by_id(frequency_id)
        return frequency
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar frequência: {str(e)}")
    
@router.post("", response_model=FrequencyResponseDTO)
async def create_frequency(dto: FrequencyCreateDTO):
    """
    Cria uma nova frequência.
    """
    try:
        frequency = await FrequencyService.create_frequency(dto)
        return frequency
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar frequência: {str(e)}")
    
@router.put("/{frequency_id}", response_model=FrequencyResponseDTO)
async def update_frequency(
    frequency_id: str = Path(..., description="ID da frequência a ser atualizada"),
    dto: FrequencyUpdateDTO = ...,
):
    """
    Atualiza uma frequência existente.
    """
    try:
        frequency = await FrequencyService.update_frequency(frequency_id, dto)
        return frequency
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar frequência: {str(e)}")
    
@router.delete("/{frequency_id}")
async def delete_frequency(
    frequency_id: str = Path(..., description="ID da frequência a ser deletada")
):
    """
    Deleta uma frequência pelo ID.
    """
    try:
        await FrequencyService.delete_frequency(frequency_id)
        return {"detail": "Frequência deletada com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar frequência: {str(e)}")