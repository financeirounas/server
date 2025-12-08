from typing import List, Optional
from fastapi import HTTPException
from lib.supabase_client import supabase
from entities.models.budgets import Budget


class BudgetRepository:
    TABLE_NAME = "budgets"

    @staticmethod
    async def create_budget(data: dict) -> Budget:
        """
        Cria um novo orçamento.
        Retorna o registro criado.
        """
        try:
            response = (
                supabase.table(BudgetRepository.TABLE_NAME)
                .insert(data)
                .execute()
            )
            if not response.data:
                raise HTTPException(
                    status_code=500,
                    detail="Erro ao criar orçamento no Supabase",
                )
            return Budget(**response.data[0])
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar orçamento: {str(e)}",
            )

    @staticmethod
    async def get_budget_by_id(budget_id: str) -> Budget:
        """
        Busca um orçamento pelo ID.
        Retorna o registro encontrado.
        """
        response = (
            supabase.table(BudgetRepository.TABLE_NAME)
            .select("*")
            .eq("id", budget_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Orçamento não encontrado")
        return Budget(**response.data[0])

    @staticmethod
    async def list_budgets(
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
    ) -> List[Budget]:
        """
        Lista todos os orçamentos, com filtros opcionais por período.
        Retorna lista de Budget.
        """
        query = supabase.table(BudgetRepository.TABLE_NAME).select("*")

        if initial_date:
            query = query.gte("initial_date", initial_date)
        if final_date:
            query = query.lte("final_date", final_date)

        response = query.execute()

        if not response.data:
            return []
        return [Budget(**item) for item in response.data]

    @staticmethod
    async def update_budget(budget_id: str, data: dict) -> Budget:
        """
        Atualiza um orçamento.
        Retorna o registro atualizado.
        """
        try:
            response = (
                supabase.table(BudgetRepository.TABLE_NAME)
                .update(data)
                .eq("id", budget_id)
                .execute()
            )
            if not response.data:
                raise HTTPException(status_code=404, detail="Orçamento não encontrado")
            return Budget(**response.data[0])
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao atualizar orçamento: {str(e)}",
            )

    @staticmethod
    async def delete_budget(budget_id: str) -> None:
        """
        Deleta um orçamento.
        Antes, valida se existem pedidos usando este orçamento.
        """
        # Verifica se existe algum pedido referenciando este orçamento
        orders_response = (
            supabase.table("orders")
            .select("id")
            .eq("budget_id", budget_id)
            .limit(1)
            .execute()
        )

        if orders_response.data:
            raise HTTPException(
                status_code=400,
                detail="Não é possível deletar o orçamento, pois existem pedidos vinculados a ele.",
            )

        # Se não houver pedidos, tenta deletar
        response = (
            supabase.table(BudgetRepository.TABLE_NAME)
            .delete()
            .eq("id", budget_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Orçamento não encontrado")
        return None