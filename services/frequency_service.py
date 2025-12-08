from typing import List, Optional
from fastapi import HTTPException
from repositories.frequency_repository import FrequencyRepository
from services.unit_user_service import to_brazil
from entities.dtos.frequency_dto import (
    FrequencyCreateDTO,
    FrequencyResponseDTO,
    FrequencyUpdateDTO,
)
from datetime import date, datetime

class FrequencyService:
    @staticmethod
    async def list_frequencies(
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        unit_id: Optional[str] = None,
    ) -> List[FrequencyResponseDTO]:
        """
        Lista todas as frequências, com filtros opcionais por período e unidade.
        Retorna lista de FrequencyResponseDTO.
        """
        frequencies = await FrequencyRepository.list_frequencies(
            initial_date=initial_date,
            final_date=final_date,
            unit_id=unit_id,
        )

        return [
            FrequencyResponseDTO(
                id=freq.id,
                unit_id=freq.unit_id,
                amount=freq.amount,
                date=freq.date.strftime("%Y-%m-%d") if isinstance(freq.date, (date, datetime)) else str(freq.date),
                updated_at=to_brazil(freq.updated_at) if freq.updated_at else None,
            )
            for freq in frequencies
        ]
    
    @staticmethod
    async def get_frequency_by_id(frequency_id: str) -> FrequencyResponseDTO:
        """
        Busca uma frequência pelo ID.
        Retorna a frequência encontrada.
        """
        frequency = await FrequencyRepository.get_frequency_by_id(frequency_id)
        return FrequencyResponseDTO(
            id=frequency.id,
            unit_id=frequency.unit_id,
            amount=frequency.amount,
            date=frequency.date.strftime("%Y-%m-%d") if isinstance(frequency.date, (date, datetime)) else str(frequency.date),
            updated_at=to_brazil(frequency.updated_at) if frequency.updated_at else None,
        )
    
    @staticmethod
    async def create_frequency(dto: FrequencyCreateDTO) -> FrequencyResponseDTO:
        """
        Cria uma nova frequência.
        Retorna a frequência criada.
        """
        # Converte o DTO para dict e garante que date seja string
        data = dto.dict()
        if 'date' in data and isinstance(data['date'], (date, datetime)):
            data['date'] = data['date'].strftime("%Y-%m-%d")
        elif 'date' in data and hasattr(data['date'], 'isoformat'):
            data['date'] = data['date'].isoformat()
        frequency = await FrequencyRepository.create_frequency(data)
        return FrequencyResponseDTO(
            id=frequency.id,
            unit_id=frequency.unit_id,
            amount=frequency.amount,
            date=frequency.date.strftime("%Y-%m-%d") if isinstance(frequency.date, (date, datetime)) else str(frequency.date),
            updated_at=to_brazil(frequency.updated_at) if frequency.updated_at else None,
        )
    
    @staticmethod
    async def update_frequency(
        frequency_id: str, dto: FrequencyUpdateDTO
    ) -> FrequencyResponseDTO:
        """
        Atualiza uma frequência.
        Retorna a frequência atualizada.
        """
        # Converte o DTO para dict e garante que date seja string
        data = dto.dict(exclude_unset=True)
        if 'date' in data and isinstance(data['date'], (date, datetime)):
            data['date'] = data['date'].strftime("%Y-%m-%d")
        elif 'date' in data and hasattr(data['date'], 'isoformat'):
            data['date'] = data['date'].isoformat()
        
        frequency = await FrequencyRepository.update_frequency(frequency_id, data)
        return FrequencyResponseDTO(
            id=frequency.id,
            unit_id=frequency.unit_id,
            amount=frequency.amount,
            date=frequency.date.strftime("%Y-%m-%d") if isinstance(frequency.date, (date, datetime)) else str(frequency.date),
            updated_at=to_brazil(frequency.updated_at) if frequency.updated_at else None,
        )
    
    @staticmethod
    async def delete_frequency(frequency_id: str) -> None:
        """
        Deleta uma frequência pelo ID.
        """
        await FrequencyRepository.delete_frequency(frequency_id)
    
    