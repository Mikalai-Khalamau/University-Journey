from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.fractal import Fractal
from src.domain.value_objects.user_stats import UserStats

class IFractalRepository(ABC):
    @abstractmethod
    def save(self, fractal: Fractal) -> Fractal:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, fractal_id: UUID, user_id: UUID) -> Fractal | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[Fractal]:
        raise NotImplementedError

    @abstractmethod
    def update_name(self, fractal_id: UUID, user_id: UUID, name: str) -> Fractal | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, fractal_id: UUID, user_id: UUID) -> bool:
        raise NotImplementedError

    def get_user_stats(self, user_id: UUID) -> UserStats:
        """Возвращает агрегированную статистику пользователя."""
        raise NotImplementedError
