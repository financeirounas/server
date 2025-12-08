from fastapi import APIRouter, HTTPException, Query
from typing import List

from services.user_service import UserService
from services.auth_service import AuthService
from entities.dtos.user_dto import UserCreateDTO, UserResponseDTO

router = APIRouter()

@router.post("/register", response_model=UserResponseDTO)
async def register_user(dto: UserCreateDTO):
    """
    Registra um novo usuário.
    Verifica se o e-mail já está em uso.
    """
    try:
        user = await UserService.register_user(
            email=dto.email,
            password=dto.password,
            username=dto.username,
            role=dto.role
        )
        if user is None:
            raise HTTPException(status_code=500, detail="Erro ao registrar usuário")
        try:
            await AuthService.send_code_verify_email(user.email)
        except Exception:
            pass
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar usuário: {str(e)}")
    
@router.get("", response_model=List[UserResponseDTO])
async def list_users(role: str | None = Query(None, description="Filtrar por tipo de usuário")):
    """
    Lista usuários com filtros opcionais.
    """
    try:
        users = await UserService.list_users(role=role)
        return [
            UserResponseDTO(
                id=user.id,
                email=user.email,
                username=user.username,
                role=user.role
            ) for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")
    
@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user_by_id(user_id: str):
    """
    Retorna um usuário pelo ID.
    """
    try:
        user = await UserService.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter usuário: {str(e)}")
    
@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(user_id: str, dto: UserCreateDTO):
    """
    Atualiza um usuário existente.
    """
    try:
        user = await UserService.update_user(
            user_id=user_id,
            username=dto.username,
            role=dto.role
        )
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {str(e)}")
    
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """
    Deleta um usuário pelo ID.
    """
    try:
        await UserService.delete_user(user_id)
        return {"detail": "Usuário deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar usuário: {str(e)}")