from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path
from entities.dtos.budgets_dto import (
    BudgetCreateDTO,
    BudgetUpdateDTO,
    BudgetResponseDTO,
)
from services.budget_service import BudgetService

router = APIRouter()


@router.get("", response_model=List[BudgetResponseDTO])
async def list_budgets(
    initial_date: Optional[str] = Query(
        None,
        description="Data inicial do período (formato YYYY-MM-DD)",
    ),
    final_date: Optional[str] = Query(
        None,
        description="Data final do período (formato YYYY-MM-DD)",
    ),
):
    """
    Lista orçamentos, com filtros opcionais por período.
    """
    try:
        return await BudgetService.list_budgets(
            initial_date=initial_date,
            final_date=final_date,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar orçamentos: {str(e)}",
        )


@router.get("/{budget_id}", response_model=BudgetResponseDTO)
async def get_budget(
    budget_id: str = Path(..., description="ID do orçamento"),
):
    """
    Busca um orçamento pelo ID.
    """
    try:
        return await BudgetService.get_budget_by_id(budget_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar orçamento: {str(e)}",
        )


@router.post("", response_model=BudgetResponseDTO, status_code=201)
async def create_budget(dto: BudgetCreateDTO):
    """
    Cria um novo orçamento.
    """
    try:
        return await BudgetService.create_budget(dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar orçamento: {str(e)}",
        )


@router.put("/{budget_id}", response_model=BudgetResponseDTO)
async def update_budget(
    budget_id: str = Path(..., description="ID do orçamento"),
    dto: BudgetUpdateDTO = ...,
):
    """
    Atualiza um orçamento existente.
    """
    try:
        return await BudgetService.update_budget(budget_id, dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar orçamento: {str(e)}",
        )


@router.delete("/{budget_id}", status_code=204)
async def delete_budget(
    budget_id: str = Path(..., description="ID do orçamento"),
):
    """
    Deleta um orçamento existente.
    """
    try:
        await BudgetService.delete_budget(budget_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar orçamento: {str(e)}",
        )