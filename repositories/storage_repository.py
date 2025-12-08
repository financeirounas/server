from typing import List, Optional
from fastapi import HTTPException
from lib.supabase_client import supabase
from entities.models.storage import Storage
from datetime import datetime, timezone


class StorageRepository:
    TABLE_NAME = "storage"

    @staticmethod
    async def get_storage_by_unit(unit_id: str) -> List[Storage]:
        """
        Busca todos os itens de estoque de uma unidade.
        Retorna lista de Storage.
        """
        response = (
            supabase.table(StorageRepository.TABLE_NAME)
            .select("*")
            .eq("unit_id", unit_id)
            .execute()
        )

        if not response.data:
            return []

        return [Storage(**item) for item in response.data]

    @staticmethod
    async def get_storage_item(unit_id: str, name: str) -> Optional[Storage]:
        """
        Busca um item específico por unidade e nome.
        Retorna Storage ou None.
        """
        response = (
            supabase.table(StorageRepository.TABLE_NAME)
            .select("*")
            .eq("unit_id", unit_id)
            .eq("name", name)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return Storage(**response.data[0])

    @staticmethod
    async def create_storage_item(
        unit_id: str,
        name: str,
        amount: float,
        type: str,
        initial_quantity: int,
    ) -> Storage:
        """
        Cria um novo item no estoque.
        Retorna o registro criado.
        """
        try:
            response = (
                supabase.table(StorageRepository.TABLE_NAME)
                .insert(
                    {
                        "unit_id": unit_id,
                        "name": name,
                        "amount": amount,
                        "type": type,
                        "initial_quantity": initial_quantity,
                        "used_quantity": 0,
                    }
                )
                .execute()
            )

            if not response.data:
                raise HTTPException(status_code=500, detail="Erro ao criar item no estoque")

            return Storage(**response.data[0])
        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()

            if (
                ("foreign key constraint" in error_lower)
                or ("23503" in error_str)
                or ("storage_unit_id_fkey" in error_lower)
                or ("violates foreign key constraint" in error_lower)
            ):
                if "unit_id" in error_lower or "units" in error_lower or "is not present in table" in error_lower:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Unidade com ID '{unit_id}' não encontrada. Verifique se o unit_id está correto e existe na tabela 'units'.",
                    )

            if isinstance(e, HTTPException):
                raise

            raise HTTPException(status_code=500, detail=f"Erro ao criar item no estoque: {str(e)}")

    @staticmethod
    async def increment_initial_quantity(storage_id: str, increment: int, new_amount: float = None, new_type: str = None) -> Storage:
        """
        Incrementa a initial_quantity de um item existente.
        Se new_amount/new_type forem passados atualiza esses campos também.
        Retorna o item atualizado.
        """
        if increment <= 0:
            raise HTTPException(status_code=400, detail="increment deve ser maior que 0")

        # pega os valores atuais
        resp = supabase.table(StorageRepository.TABLE_NAME).select("*").eq("id", storage_id).limit(1).execute()
        if not resp.data:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        current = resp.data[0]
        new_initial = (current.get("initial_quantity") or 0) + increment

        update_payload = {"initial_quantity": new_initial, "updated_at": datetime.now(timezone.utc).isoformat()}
        if new_amount is not None:
            update_payload["amount"] = new_amount
        if new_type is not None:
            update_payload["type"] = new_type

        response = (
            supabase.table(StorageRepository.TABLE_NAME)
            .update(update_payload)
            .eq("id", storage_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao incrementar quantidade no estoque")

        return Storage(**response.data[0])

    @staticmethod
    async def update_storage_used_quantity(storage_id: str, new_used_quantity: int) -> Storage:
        """
        Atualiza a quantidade utilizada de um item no estoque para um valor absoluto.
        Retorna o registro atualizado.
        """
        # busca initial_quantity e used_quantity atuais
        resp = supabase.table(StorageRepository.TABLE_NAME).select("initial_quantity", "used_quantity").eq("id", storage_id).limit(1).execute()
        if not resp.data:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        row = resp.data[0]
        initial_quantity = row.get("initial_quantity", 0)
        # valida novo valor absoluto
        if new_used_quantity < 0:
            raise HTTPException(status_code=400, detail="new_used_quantity não pode ser negativo")

        if new_used_quantity > initial_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Quantidade utilizada excede a quantidade inicial. Inicial: {initial_quantity}, Solicitada: {new_used_quantity}",
            )

        now = datetime.now(timezone.utc)
        response = (
            supabase.table(StorageRepository.TABLE_NAME)
            .update({"used_quantity": new_used_quantity, "updated_at": now.isoformat()})
            .eq("id", storage_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar quantidade no estoque")

        return Storage(**response.data[0])
