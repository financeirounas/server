from typing import List, Optional
from fastapi import HTTPException
from lib.supabase_client import supabase
from entities.models.orders import Order
from entities.models.order_item import OrderItem

class OrderRepository:
    TABLE_NAME = "orders"

    @staticmethod
    async def create_order(data: dict) -> Order:
        """
        Cria um novo pedido.
        Retorna o registro criado.
        """
        try:
            response = (
                supabase.table(OrderRepository.TABLE_NAME)
                .insert(data)
                .execute()
            )
            if not response.data:
                raise HTTPException(status_code=500, detail="Erro ao criar pedido no Supabase")
            return Order(**response.data[0])
        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()
            
            # Verifica erros de foreign key constraint
            if ("foreign key constraint" in error_lower or 
                "23503" in error_str or 
                "violates foreign key constraint" in error_lower):
                if "unit_id" in error_lower or "units" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Unidade com ID '{data.get('unit_id')}' não encontrada."
                    )
                if "budget_id" in error_lower or "budgets" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Orçamento com ID '{data.get('budget_id')}' não encontrado."
                    )
            
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")

    @staticmethod
    async def get_order_by_id(order_id: str) -> Order:
        """
        Busca um pedido pelo ID.
        Retorna o registro encontrado.
        """
        response = (
            supabase.table(OrderRepository.TABLE_NAME)
            .select("*")
            .eq("id", order_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return Order(**response.data[0])
    
    @staticmethod
    async def list_orders(
        unit_id: Optional[str] = None,
        budget_id: Optional[str] = None
    ) -> List[Order]:
        """
        Lista todos os pedidos, com filtros opcionais.
        Retorna lista de pedidos.
        """
        query = supabase.table(OrderRepository.TABLE_NAME).select("*")
        
        if unit_id:
            query = query.eq("unit_id", unit_id)
        if budget_id:
            query = query.eq("budget_id", budget_id)
        
        response = query.execute()
        
        if not response.data:
            return []
        return [Order(**item) for item in response.data]

    @staticmethod
    async def update_order(order_id: str, data: dict) -> Order:
        """
        Atualiza um pedido.
        Retorna o registro atualizado.
        """
        try:
            response = (
                supabase.table(OrderRepository.TABLE_NAME)
                .update(data)
                .eq("id", order_id)
                .execute()
            )
            if not response.data:
                raise HTTPException(status_code=404, detail="Pedido não encontrado")
            return Order(**response.data[0])
        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()
            
            # Verifica erros de foreign key constraint
            if ("foreign key constraint" in error_lower or 
                "23503" in error_str or 
                "violates foreign key constraint" in error_lower):
                if "unit_id" in error_lower or "units" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Unidade com ID '{data.get('unit_id')}' não encontrada."
                    )
                if "budget_id" in error_lower or "budgets" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Orçamento com ID '{data.get('budget_id')}' não encontrado."
                    )
            
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

    @staticmethod
    async def delete_order(order_id: str) -> None:
        """
        Deleta um pedido.
        """
        response = (
            supabase.table(OrderRepository.TABLE_NAME)
            .delete()
            .eq("id", order_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return None

    @staticmethod
    async def get_orders_by_unit_id(unit_id: str) -> List[Order]:
        """
        Busca todos os pedidos de uma unidade.
        Retorna lista de Order.
        """
        return await OrderRepository.list_orders(unit_id=unit_id)

    @staticmethod
    async def get_orders_by_budget_id(budget_id: str) -> List[Order]:
        """
        Busca todos os pedidos de um orçamento.
        Retorna lista de Order.
        """
        return await OrderRepository.list_orders(budget_id=budget_id)

class OrderItemRepository:
    TABLE_NAME = "order_items"

    @staticmethod
    async def create_order_item(data: dict) -> OrderItem:
        """
        Cria um novo item de pedido.
        Retorna o registro criado.
        """
        try:
            response = (
                supabase.table(OrderItemRepository.TABLE_NAME)
                .insert(data)
                .execute()
            )
            if not response.data:
                raise HTTPException(status_code=500, detail="Erro ao criar item de pedido no Supabase")
            return OrderItem(**response.data[0])
        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()
            
            # Verifica erros de foreign key constraint
            if ("foreign key constraint" in error_lower or 
                "23503" in error_str or 
                "violates foreign key constraint" in error_lower):
                if "order_id" in error_lower or "orders" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Pedido com ID '{data.get('order_id')}' não encontrado."
                    )
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Erro ao criar item de pedido: {str(e)}")

    @staticmethod
    async def get_order_item_by_id(order_item_id: str) -> Optional[OrderItem]:
        """
        Busca um item de pedido pelo ID.
        Retorna OrderItem ou None se não encontrado.
        """
        response = (
            supabase.table(OrderItemRepository.TABLE_NAME)
            .select("*")
            .eq("id", order_item_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return OrderItem(**response.data[0])

    @staticmethod
    async def get_order_items_by_order_id(order_id: str) -> List[OrderItem]:
        """
        Busca todos os itens de um pedido.
        Retorna lista de OrderItem.
        """
        response = (
            supabase.table(OrderItemRepository.TABLE_NAME)
            .select("*")
            .eq("order_id", order_id)
            .execute()
        )
        if not response.data:
            return []
        return [OrderItem(**item) for item in response.data]

    @staticmethod
    async def update_order_item(order_item_id: str, data: dict) -> OrderItem:
        """
        Atualiza um item de pedido.
        Retorna o registro atualizado.
        """
        try:
            response = (
                supabase.table(OrderItemRepository.TABLE_NAME)
                .update(data)
                .eq("id", order_item_id)
                .execute()
            )
            if not response.data:
                raise HTTPException(status_code=404, detail="Item de pedido não encontrado")
            return OrderItem(**response.data[0])
        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()
            
            # Verifica erros de foreign key constraint
            if ("foreign key constraint" in error_lower or 
                "23503" in error_str or 
                "violates foreign key constraint" in error_lower):
                if "order_id" in error_lower or "orders" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Pedido com ID '{data.get('order_id')}' não encontrado."
                    )
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar item de pedido: {str(e)}")

    @staticmethod
    async def delete_order_item(order_item_id: str) -> None:
        """
        Deleta um item de pedido.
        """
        response = (
            supabase.table(OrderItemRepository.TABLE_NAME)
            .delete()
            .eq("id", order_item_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Item de pedido não encontrado")
        return None

    @staticmethod
    async def delete_order_items_by_order_id(order_id: str) -> None:
        """
        Deleta todos os itens de um pedido.
        """
        response = (
            supabase.table(OrderItemRepository.TABLE_NAME)
            .delete()
            .eq("order_id", order_id)
            .execute()
        )
        return None
        
        