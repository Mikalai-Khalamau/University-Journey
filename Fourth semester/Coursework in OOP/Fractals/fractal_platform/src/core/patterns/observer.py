from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, event_name: str, payload: dict) -> None:
        raise NotImplementedError


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event_name: str, payload: dict) -> None:
        for observer in self._observers:
            observer.update(event_name, payload)
