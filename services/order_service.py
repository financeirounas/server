from typing import List, Optional
from fastapi import HTTPException
from repositories.order_repository import OrderRepository, OrderItemRepository
from entities.dtos.orders_dto import (
    OrderCreateDTO,
    OrderUpdateDTO,
    OrderResponseDTO,
    OrderItemCreateDTO,
    OrderItemResponseDTO,
)

class OrderService:

    @staticmethod
    async def list_orders(
        unit_id: Optional[str] = None,
        budget_id: Optional[str] = None
    ) -> List[OrderResponseDTO]:
        """
        Lista todos os pedidos, com filtros opcionais.
        Retorna lista de OrderResponseDTO.
        """
        orders = await OrderRepository.list_orders(unit_id=unit_id, budget_id=budget_id)
        
        

        result = []
        for order in orders:
            
            items = await OrderItemRepository.get_order_items_by_order_id(order.id)

            result.append(OrderResponseDTO(
                id=order.id,
                description=order.description,
                amount=order.amount,
                unit_id=order.unit_id,
                budget_id=order.budget_id,
                status=order.status if hasattr(order, 'status') else None,
                created_at=order.created_at.isoformat() if order.created_at else None,
                items=[
                    OrderItemResponseDTO(
                        id=item.id,
                        description=item.description,
                        amount=item.amount,
                        measure_unit=item.measure_unit,
                        received=item.received,
                        order_id=item.order_id,
                        created_at=item.created_at.isoformat() if item.created_at else None,
                        quantity= item.quantity if hasattr(item, 'quantity') else None,
                    )
                    for item in items
                ] if items else None
            ))

        return result

    @staticmethod
    async def get_order_by_id(order_id: str) -> OrderResponseDTO:
        """
        Busca um pedido pelo ID.
        Retorna OrderResponseDTO com os itens do pedido.
        """
        try:
            order = await OrderRepository.get_order_by_id(order_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {str(e)}")

        items = await OrderItemRepository.get_order_items_by_order_id(order.id)

        return OrderResponseDTO(
            id=order.id,
            description=order.description,
            amount=order.amount,
            unit_id=order.unit_id,
            budget_id=order.budget_id,
            status=order.status if hasattr(order, 'status') else None,
            created_at=order.created_at.isoformat() if order.created_at else None,
            items=[
                OrderItemResponseDTO(
                    id=item.id,
                    description=item.description,
                    amount=item.amount,
                    measure_unit=item.measure_unit,
                    received=item.received,
                    order_id=item.order_id,
                    created_at=item.created_at.isoformat() if item.created_at else None,
                )
                for item in items
            ] if items else None
        )

    @staticmethod
    async def create_order(dto: OrderCreateDTO) -> OrderResponseDTO:
        """
        Cria um novo pedido.
        Retorna OrderResponseDTO.
        """
        try:
            # prepara os dados do pedido (exclui items que não vai para a tabela orders)
            order_data = {
                "description": dto.description,
                "amount": dto.amount,
                "unit_id": dto.unit_id,
                "budget_id": dto.budget_id,
            }
            # Remove keys com valor None
            order_data = {k: v for k, v in order_data.items() if v is not None}

            # cria o pedido
            order = await OrderRepository.create_order(order_data)

            # cria os itens do pedido, se fornecidos
            if dto.items:
                for item_dto in dto.items:
                    item_data = {
                        "order_id": order.id,
                        "description": item_dto.description,
                        "amount": item_dto.amount,
                        "measure_unit": item_dto.measure_unit if item_dto.measure_unit else "pacote",
                        "received": item_dto.received if item_dto.received is not None else True,
                    }
                    # remove None values
                    item_data = {k: v for k, v in item_data.items() if v is not None}

                    await OrderItemRepository.create_order_item(item_data)

            # busca todos os itens do pedido (para garantir que está completo)
            all_items = await OrderItemRepository.get_order_items_by_order_id(order.id)
            
            # Calcula o total automaticamente se não foi fornecido e há itens
            calculated_amount = order.amount
            if not calculated_amount and all_items:
                calculated_amount = sum(item.amount for item in all_items)
                # Atualiza o pedido com o total calculado
                if calculated_amount:
                    await OrderRepository.update_order(order.id, {"amount": calculated_amount})
                    order.amount = calculated_amount

            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                amount=order.amount,
                unit_id=order.unit_id,
                budget_id=order.budget_id,
                status=order.status if hasattr(order, 'status') else None,
                created_at=order.created_at.isoformat() if order.created_at else None,
                items=[
                    OrderItemResponseDTO(
                        id=item.id,
                        description=item.description,
                        amount=item.amount,
                        measure_unit=item.measure_unit,
                        received=item.received,
                        order_id=item.order_id,
                        created_at=item.created_at.isoformat() if item.created_at else None,
                    )
                    for item in all_items
                ] if all_items else None
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")

    @staticmethod
    async def update_order(order_id: str, dto: OrderUpdateDTO) -> OrderResponseDTO:
        """
        Atualiza um pedido existente.
        Retorna OrderResponseDTO atualizado.
        """
        try:
            # exclude_unset=True para não sobrescrever com None campos não enviados
            data = dto.model_dump(exclude_unset=True)
            order = await OrderRepository.update_order(order_id, data)

            # busca os itens do pedido
            items = await OrderItemRepository.get_order_items_by_order_id(order.id)

            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                amount=order.amount,
                unit_id=order.unit_id,
                budget_id=order.budget_id,
                status=order.status if hasattr(order, 'status') else None,
                created_at=order.created_at.isoformat() if order.created_at else None,
                items=[
                    OrderItemResponseDTO(
                        id=item.id,
                        description=item.description,
                        amount=item.amount,
                        measure_unit=item.measure_unit,
                        received=item.received,
                        order_id=item.order_id,
                        created_at=item.created_at.isoformat() if item.created_at else None,
                    )
                    for item in items
                ] if items else None
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")
    
    @staticmethod
    async def delete_order(order_id: str) -> None:
        """
        Deleta um pedido existente.
        Retorna None.
        """
        try:
            # Deleta os itens primeiro para evitar erro de foreign key constraint
            await OrderItemRepository.delete_order_items_by_order_id(order_id)
            # Depois deleta o pedido
            await OrderRepository.delete_order(order_id)
            return None
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar pedido: {str(e)}")

    @staticmethod
    async def get_orders_by_unit_id(unit_id: str) -> List[OrderResponseDTO]:
        """
        Busca todos os pedidos de uma unidade.
        Retorna lista de OrderResponseDTO.
        """
        return await OrderService.list_orders(unit_id=unit_id)

    
    @staticmethod
    async def get_orders_by_budget_id(budget_id: str) -> List[OrderResponseDTO]:
        """
        Busca todos os pedidos de um orçamento.
        Retorna lista de OrderResponseDTO.
        """
        return await OrderService.list_orders(budget_id=budget_id)

    @staticmethod
    async def approve_order(order_id: str) -> OrderResponseDTO:
        """
        Aprova um pedido.
        Atualiza o status para 'approved'.
        Retorna OrderResponseDTO atualizado.
        """
        try:
            data = {"status": "approved"}
            order = await OrderRepository.update_order(order_id, data)
            
            items = await OrderItemRepository.get_order_items_by_order_id(order.id)
            
            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                amount=order.amount,
                unit_id=order.unit_id,
                budget_id=order.budget_id,
                status=order.status if hasattr(order, 'status') else "approved",
                created_at=order.created_at.isoformat() if order.created_at else None,
                items=[
                    OrderItemResponseDTO(
                        id=item.id,
                        description=item.description,
                        amount=item.amount,
                        measure_unit=item.measure_unit,
                        received=item.received,
                        order_id=item.order_id,
                        created_at=item.created_at.isoformat() if item.created_at else None,
                    )
                    for item in items
                ] if items else None
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao aprovar pedido: {str(e)}")

    @staticmethod
    async def reject_order(order_id: str) -> OrderResponseDTO:
        """
        Rejeita um pedido.
        Atualiza o status para 'rejected'.
        Retorna OrderResponseDTO atualizado.
        """
        try:
            data = {"status": "rejected"}
            order = await OrderRepository.update_order(order_id, data)
            
            items = await OrderItemRepository.get_order_items_by_order_id(order.id)
            
            return OrderResponseDTO(
                id=order.id,
                description=order.description,
                amount=order.amount,
                unit_id=order.unit_id,
                budget_id=order.budget_id,
                status=order.status if hasattr(order, 'status') else "rejected",
                created_at=order.created_at.isoformat() if order.created_at else None,
                items=[
                    OrderItemResponseDTO(
                        id=item.id,
                        description=item.description,
                        amount=item.amount,
                        measure_unit=item.measure_unit,
                        received=item.received,
                        order_id=item.order_id,
                        created_at=item.created_at.isoformat() if item.created_at else None,
                    )
                    for item in items
                ] if items else None
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao rejeitar pedido: {str(e)}")