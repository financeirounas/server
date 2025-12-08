from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path
from entities.dtos.orders_dto import (
    OrderCreateDTO,
    OrderUpdateDTO,
    OrderResponseDTO,
)
from services.order_service import OrderService

router = APIRouter()


@router.get("", response_model=List[OrderResponseDTO])
async def list_orders(
    unit_id: Optional[str] = Query(
        None,
        description="Filtra por ID da unidade",
    ),
    budget_id: Optional[str] = Query(
        None,
        description="Filtra por ID do orçamento",
    ),
):
    """
    Lista todos os pedidos, com filtros opcionais por unidade e orçamento.
    """
    try:
        return await OrderService.list_orders(unit_id=unit_id, budget_id=budget_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar pedidos: {str(e)}",
        )


@router.get("/{order_id}", response_model=OrderResponseDTO)
async def get_order(
    order_id: str = Path(..., description="ID do pedido"),
):
    """
    Busca um pedido pelo ID.
    """
    try:
        return await OrderService.get_order_by_id(order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar pedido: {str(e)}",
        )


@router.post("", response_model=OrderResponseDTO, status_code=201)
async def create_order(dto: OrderCreateDTO):
    """
    Cria um novo pedido.
    Pode incluir itens do pedido no campo 'items'.
    """
    try:
        return await OrderService.create_order(dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar pedido: {str(e)}",
        )


@router.put("/{order_id}", response_model=OrderResponseDTO)
async def update_order(
    order_id: str = Path(..., description="ID do pedido"),
    dto: OrderUpdateDTO = ...,
):
    """
    Atualiza os dados de um pedido.
    """
    try:
        return await OrderService.update_order(order_id, dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar pedido: {str(e)}",
        )


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: str = Path(..., description="ID do pedido"),
):
    """
    Remove um pedido e todos os seus itens.
    """
    try:
        await OrderService.delete_order(order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar pedido: {str(e)}",
        )


@router.get("/unit/{unit_id}", response_model=List[OrderResponseDTO])
async def get_orders_by_unit(
    unit_id: str = Path(..., description="ID da unidade"),
):
    """
    Busca todos os pedidos de uma unidade.
    """
    try:
        
        print(unit_id)
        return await OrderService.get_orders_by_unit_id(unit_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar pedidos da unidade: {str(e)}",
        )


@router.get("/budget/{budget_id}", response_model=List[OrderResponseDTO])
async def get_orders_by_budget(
    budget_id: str = Path(..., description="ID do orçamento"),
):
    """
    Busca todos os pedidos de um orçamento.
    """
    try:
        return await OrderService.get_orders_by_budget_id(budget_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar pedidos do orçamento: {str(e)}",
        )


@router.put("/{order_id}/approve", response_model=OrderResponseDTO)
async def approve_order(
    order_id: str = Path(..., description="ID do pedido"),
):
    """
    Aprova um pedido.
    Atualiza o status do pedido para 'approved'.
    """
    try:
        return await OrderService.approve_order(order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao aprovar pedido: {str(e)}",
        )


@router.put("/{order_id}/reject", response_model=OrderResponseDTO)
async def reject_order(
    order_id: str = Path(..., description="ID do pedido"),
):
    """
    Rejeita um pedido.
    Atualiza o status do pedido para 'rejected'.
    """
    try:
        return await OrderService.reject_order(order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao rejeitar pedido: {str(e)}",
        )