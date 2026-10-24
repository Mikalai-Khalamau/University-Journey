from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ISpecification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, item: T) -> bool:
        raise NotImplementedError
