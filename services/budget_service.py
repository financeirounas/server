from typing import List, Optional
from fastapi import HTTPException
from repositories.budgets_repository import BudgetRepository
from entities.dtos.budgets_dto import (
    BudgetCreateDTO,
    BudgetUpdateDTO,
    BudgetResponseDTO,
)

class BudgetService:

    @staticmethod
    async def list_budgets(
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
    ) -> List[BudgetResponseDTO]:
        """
        Lista orçamentos, com filtros opcionais por período.
        """
        budgets = await BudgetRepository.list_budgets(
            initial_date=initial_date,
            final_date=final_date,
        )

        return [
            BudgetResponseDTO(
                id=b.id,
                description=b.description,
                initial_date=b.initial_date,
                final_date=b.final_date,
                amount=b.amount,
                created_at=b.created_at.isoformat() if b.created_at else None,
                updated_at=b.updated_at.isoformat() if b.updated_at else None,
            )
            for b in budgets
        ]
    
    @staticmethod
    async def get_budget_by_id(budget_id: str) -> BudgetResponseDTO:
        """
        Busca um orçamento pelo ID.
        Retorna o orçamento encontrado.
        """
        budget = await BudgetRepository.get_budget_by_id(budget_id)
        return BudgetResponseDTO(
            id=budget.id,
            description=budget.description,
            initial_date=budget.initial_date,
            final_date=budget.final_date,
            amount=budget.amount,
            created_at=budget.created_at.isoformat() if budget.created_at else None,
            updated_at=budget.updated_at.isoformat() if budget.updated_at else None,
        )

    @staticmethod
    async def create_budget(dto: BudgetCreateDTO) -> BudgetResponseDTO:
        """
        Cria um novo orçamento.
        Retorna o orçamento criado.
        """
        # Usa modo JSON para serializar campos de data em string ISO para o Supabase
        data = dto.model_dump(mode="json")

        created_budget = await BudgetRepository.create_budget(data)
        return BudgetResponseDTO(
            id=created_budget.id,
            description=created_budget.description,
            initial_date=created_budget.initial_date,
            final_date=created_budget.final_date,
            amount=created_budget.amount,
            created_at=created_budget.created_at.isoformat() if created_budget.created_at else None,
            updated_at=created_budget.updated_at.isoformat() if created_budget.updated_at else None,
        )
    
    @staticmethod
    async def update_budget(budget_id: str, dto: BudgetUpdateDTO) -> BudgetResponseDTO:
        """
        Atualiza um orçamento existente.
        Aplica validações de datas e amount.
        """
        # exclude_unset=True para update parcial e mode="json" para serializar datas
        data = dto.model_dump(exclude_unset=True, mode="json")

        # Validações de domínio (com base no que veio no DTO)
        initial_date = data.get("initial_date")
        final_date = data.get("final_date")
        amount = data.get("amount")

        if amount is not None and amount < 0:
            raise HTTPException(
                status_code=400,
                detail="O valor do orçamento (amount) deve ser positivo.",
            )

        if initial_date and final_date and final_date < initial_date:
            raise HTTPException(
                status_code=400,
                detail="A data final deve ser posterior ou igual à data inicial.",
            )

        budget = await BudgetRepository.update_budget(budget_id, data)

        return BudgetResponseDTO(
            id=budget.id,
            description=budget.description,
            initial_date=budget.initial_date,
            final_date=budget.final_date,
            amount=budget.amount,
            created_at=budget.created_at.isoformat() if budget.created_at else None,
            updated_at=budget.updated_at.isoformat() if budget.updated_at else None,
        )

    @staticmethod
    async def delete_budget(budget_id: str) -> None:
        """
        Deleta um orçamento existente.
        Valida se há pedidos associados antes de deletar.
        Retorna None.
        """
        await BudgetRepository.delete_budget(budget_id)