from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date as date_type

class OrderItemCreateDTO(BaseModel):
    description: Optional[str] = Field(None, description="Descrição do item")
    amount: float = Field(..., description="Quantidade do item")
    measure_unit: Optional[str] = Field(default="pacote", description="Unidade de medida do item")
    received: Optional[bool] = Field(default=True, description="Indica se o item foi recebido")

class OrderItemResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do item do pedido")
    description: Optional[str] = Field(None, description="Descrição do item")
    amount: float = Field(..., description="Quantidade do item")
    measure_unit: str = Field(..., description="Unidade de medida do item")
    received: bool = Field(..., description="Indica se o item foi recebido")
    order_id: str = Field(..., description="Identificador do pedido")
    created_at: str = Field(..., description="Data de criação")

class OrderCreateDTO(BaseModel):
    description: Optional[str] = Field(None, description="Descrição do pedido")
    amount: Optional[float] = Field(None, description="Quantidade total do pedido")
    unit_id: Optional[str] = Field(None, description="Identificador da unidade")
    budget_id: Optional[str] = Field(None, description="Identificador do orçamento")
    items: Optional[List[OrderItemCreateDTO]] = Field(None, description="Lista de itens do pedido")

class OrderUpdateDTO(BaseModel):
    description: Optional[str] = Field(None, description="Descrição do pedido")
    amount: Optional[float] = Field(None, description="Quantidade total do pedido")
    unit_id: Optional[str] = Field(None, description="Identificador da unidade")
    budget_id: Optional[str] = Field(None, description="Identificador do orçamento")
    status: Optional[str] = Field(None, description="Status do pedido (pending, approved, rejected, completed)")

class OrderResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do pedido")
    description: Optional[str] = Field(None, description="Descrição do pedido")
    amount: Optional[float] = Field(None, description="Quantidade total do pedido")
    unit_id: Optional[str] = Field(None, description="Identificador da unidade")
    budget_id: Optional[str] = Field(None, description="Identificador do orçamento")
    status: Optional[str] = Field(None, description="Status do pedido (pending, approved, rejected, completed)")
    created_at: str = Field(..., description="Data de criação")
    items: Optional[List[OrderItemResponseDTO]] = Field(None, description="Lista de itens do pedido")
    