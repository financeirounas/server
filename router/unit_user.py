from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path
from entities.dtos.unit_user_dto import UnitUserCreateDTO, UnitUserResponseDTO, UnitUserUpdateDTO
from services.unit_user_service import UnitUserService
from entities.dtos.unit_dto import UnitResponseDTO
from entities.dtos.user_dto import UserResponseDTO

router = APIRouter()

@router.post("", response_model=UnitUserResponseDTO, status_code=201)
async def create_unit_user(dto: UnitUserCreateDTO):
    """
    Cria uma nova associação entre usuário e unidade.
    Verifica existência de usuário e unidade, além de duplicatas.
    """
    try:
        return await UnitUserService.create_unit_user(dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar associação usuário-unidade: {str(e)}",
        )
    
@router.get("", response_model=List[UnitUserResponseDTO])
async def list_unit_users():
    """
    Lista todas as associações entre usuários e unidades.
    """
    try:
        return await UnitUserService.list_all_unit_users()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar associações usuário-unidade: {str(e)}",
        )
    
@router.put("/{unit_user_id}", response_model=UnitUserResponseDTO)
async def update_unit_user(
    unit_user_id: str = Path(..., description="ID da associação usuário-unidade"),
    dto: UnitUserUpdateDTO = ...,
):
    """
    Atualiza uma associação entre usuário e unidade.
    Atualmente, apenas o campo 'role' é atualizável.
    """
    try:
        return await UnitUserService.update_unit_user(unit_user_id, dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar associação usuário-unidade: {str(e)}",
        )

@router.delete("/{unit_user_id}", status_code=204)
async def delete_unit_user(
    unit_user_id: str = Path(..., description="ID da associação usuário-unidade"),
):
    """
    Deleta uma associação entre usuário e unidade pelo ID.
    """
    try:
        await UnitUserService.delete_unit_user(unit_user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar associação usuário-unidade: {str(e)}",
        )
    
@router.get("/{unit_user_id}", response_model=UnitUserResponseDTO)
async def get_unit_user_by_id(
    unit_user_id: str = Path(..., description="ID da associação usuário-unidade"),
):
    """
    Busca uma associação entre usuário e unidade pelo ID.
    """
    try:
        return await UnitUserService.get_unit_user_by_id(unit_user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar associação usuário-unidade: {str(e)}",
        )
    
@router.get("/{user_id}/units", response_model=List[UnitResponseDTO])
async def list_unit_by_user(
    user_id: str = Path(..., description="ID do usuário"),
):
    """
    Lista todas as associações entre um usuário específico e suas unidades.
    """
    try:
        return await UnitUserService.list_unit_by_user(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar associações usuário-unidade para o usuário: {str(e)}",
        )
    
@router.get("/{unit_id}/users", response_model=List[UserResponseDTO])
async def list_users_by_unit(
    unit_id: str = Path(..., description="ID da unidade"),
):
    """
    Lista todas as associações entre uma unidade específica e seus usuários.
    """
    try:
        return await UnitUserService.list_users_by_unit(unit_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar associações usuário-unidade para a unidade: {str(e)}",
        )
    