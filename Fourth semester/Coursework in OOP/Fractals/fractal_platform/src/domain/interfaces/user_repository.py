from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError
