from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import date as date_type


class StorageItemDTO(BaseModel):
    name: str = Field(..., description="Nome do item")
    amount: float = Field(..., gt=0, description="Preço do item")
    initial_quantity: int = Field(..., ge=0, description="Quantidade inicial do item")
    used_quantity: int = Field(..., ge=0, description="Quantidade já utilizada do item")

    @model_validator(mode="after")
    def validate_quantities(self):
        if self.used_quantity > self.initial_quantity:
            raise ValueError("used_quantity não pode ser maior que initial_quantity")
        return self


class StorageEntryDTO(BaseModel):
    name: str = Field(..., description="Nome do item")
    amount: float = Field(..., gt=0, description="Preço do item")
    unit_id: str = Field(..., description="Identificador da unidade")
    type: str = Field(..., description="Tipo de entrada (comprado ou doado)")
    supplier: Optional[str] = Field(None, description="Nome do fornecedor ou doador")
    invoice: Optional[str] = Field(None, description="Número da nota fiscal")
    responsible: str = Field(..., description="Nome do responsável")
    date: date_type = Field(..., description="Data da entrada")
    initial_quantity: int = Field(..., ge=0, description="Quantidade inicial do item")
    used_quantity: int = Field(0, ge=0, description="Quantidade já utilizada do item (default 0)")

    @model_validator(mode="after")
    def validate_quantities(self):
        if self.used_quantity > self.initial_quantity:
            raise ValueError("used_quantity não pode ser maior que initial_quantity")
        return self


class StorageExitItemDTO(BaseModel):
    name: str = Field(..., description="Nome do item")
    used_quantity: int = Field(..., ge=1, description="Quantidade a consumir do estoque (inteiro > 0)")


class StorageExitDTO(BaseModel):
    items: List[StorageExitItemDTO] = Field(..., description="Lista de itens para saída")
    purpose: str = Field(..., description="Finalidade da saída")
    responsible: str = Field(..., description="Nome do responsável")
    date: date_type = Field(..., description="Data da saída")
    notes: Optional[str] = Field(None, description="Observações adicionais")
    unit_id: str = Field(..., description="Identificador da unidade")


class StorageResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do item")
    name: str = Field(..., description="Nome do item")
    amount: float = Field(..., description="Preço do item")
    unit_id: str = Field(..., description="Identificador da unidade")
    type: str = Field(..., description="Tipo de entrada")
    created_at: Optional[str] = Field(None, description="Data de criação (ISO)")
    updated_at: Optional[str] = Field(None, description="Data de atualização (ISO)")
    initial_quantity: int = Field(..., description="Quantidade inicial do item no estoque")
    used_quantity: int = Field(..., description="Quantidade já utilizada do item no estoque")
    current_quantity: int = Field(..., description="Quantidade atual (initial_quantity - used_quantity)")
