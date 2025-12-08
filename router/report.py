from typing import Optional
from fastapi import APIRouter, Query, Path, Depends, HTTPException, status, Header

# DTO do relatório
from entities.dtos.report_dto import ReportByUnit
from entities.dtos.user_dto import UserResponseDTO as UserDTO
from services.reports_service import ReportsService
from services.unit_user_service import UnitUserService
from services.jwt_service import JWTService
from repositories.user_repository import UserRepository

router = APIRouter()


async def get_current_user(authorization: str = Header(None)) -> UserDTO:
    """
    Dependência simples para resolver o usuário atual a partir do header Authorization: "Bearer <token>".
    Retorna um UserResponseDTO se válido, ou levanta HTTPException(401).
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = parts[1]
    user_id = await JWTService.get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_record = await UserRepository.get_user("id", user_id)
    if not user_record:
        raise HTTPException(status_code=401, detail="User not found")
    return UserDTO(
        id=str(getattr(user_record, "id", "")),
        email=getattr(user_record, "email", ""),
        username=getattr(user_record, "username", getattr(user_record, "name", "")),
        role=getattr(user_record, "role", "")
    )

@router.get("/unit/{unit_id}", response_model=ReportByUnit)
async def get_report_by_unit(
    unit_id: str = Path(..., description="ID da unidade (unit_id)"),
    month: Optional[str] = Query(None, description="Período no formato YYYY-MM (opcional)"),
):
    """
    Retorna o relatório da unidade especificada.
    `month` (opcional) deve vir no formato "YYYY-MM". Se omisso, é usado o período padrão (todos os dados / acumulado).
    """
    try:
        report = await ReportsService.generate_unit_report(unit_id=unit_id, month=month)
        return report
    except HTTPException:
        raise
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")


@router.get("/me", response_model=ReportByUnit)
async def get_my_unit_report(
    month: Optional[str] = Query(None, description="Período no formato YYYY-MM (opcional)"),
    current_user: UserDTO = Depends(get_current_user),
):
    """
    Resolve a unidade do usuário autenticado e retorna o relatório dessa unidade.
    Regras:
      - tenta buscar as units associadas ao usuário via UnitUserService e seleciona a primeira (ou a default).
      - se não for possível resolver a unidade, retorna 404.
    """
    if UnitUserService is None:
        raise HTTPException(status_code=501, detail="Serviço de associação usuário-unidade não configurado")

    try:
        # espera que UnitUserService.list_units_for_user retorne lista de Unit DTOs ou registros com 'id'
        units = await UnitUserService.list_unit_by_user(getattr(current_user, "id", None))
        if not units:
            raise HTTPException(status_code=404, detail="Nenhuma unidade associada ao usuário")
        # política simples: pega a primeira unit associada (você pode alterar para escolher a default)
        unit_id = getattr(units[0], "id", None)
        if not unit_id:
            raise HTTPException(status_code=500, detail="Formato inesperado ao recuperar unidades do usuário")
        report = await ReportsService.generate_unit_report(unit_id=unit_id, month=month)
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar relatório do usuário: {str(e)}")
