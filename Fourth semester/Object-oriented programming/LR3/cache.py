from abc import ABC, abstractmethod
from collections import OrderedDict, deque
from typing import Optional, Dict

class EvictionStrategy(ABC):
    """Абстрактный класс стратегии вытеснения."""

    @abstractmethod
    def should_evict(self, cache_data: dict, max_size: int) -> Optional[str]:
        """Возвращает ключ элемента, который нужно удалить, или None."""
        pass

    @abstractmethod
    def on_access(self, cache_data: dict, key: str) -> None:
        """Вызывается при обращении к элементу."""
        pass

    @abstractmethod
    def on_add(self, cache_data: dict, key: str) -> None:
        """Вызывается при добавлении нового элемента."""
        pass

    @abstractmethod
    def on_remove(self, cache_data: dict, key: str) -> None:
        """Вызывается при удалении элемента."""
        pass


class LRUStrategy(EvictionStrategy):
    """Least Recently Used — вытесняет наименее недавно использованный."""

    def __init__(self):
        self._order = OrderedDict()

    def should_evict(self, cache_data: dict, max_size: int) -> Optional[str]:
        if len(cache_data) >= max_size and self._order:
            return next(iter(self._order))
        return None

    def on_access(self, cache_data: dict, key: str) -> None:
        if key in self._order:
            self._order.move_to_end(key)

    def on_add(self, cache_data: dict, key: str) -> None:
        self._order[key] = True
        self._order.move_to_end(key)

    def on_remove(self, cache_data: dict, key: str) -> None:
        self._order.pop(key, None)


class FIFOStrategy(EvictionStrategy):
    """First In, First Out — вытесняет самый первый добавленный."""

    def __init__(self):
        self._queue = deque()

    def should_evict(self, cache_data: dict, max_size: int) -> Optional[str]:
        if len(cache_data) >= max_size and self._queue:
            return self._queue[0]
        return None

    def on_access(self, cache_data: dict, key: str) -> None:
        pass

    def on_add(self, cache_data: dict, key: str) -> None:
        self._queue.append(key)

    def on_remove(self, cache_data: dict, key: str) -> None:
        try:
            self._queue.remove(key)
        except ValueError:
            pass


class LFUStrategy(EvictionStrategy):
    """Least Frequently Used — вытесняет самый редко используемый."""

    def __init__(self):
        self._freq: Dict[str, int] = {}

    def should_evict(self, cache_data: dict, max_size: int) -> Optional[str]:
        if len(cache_data) >= max_size and self._freq:
            return min(self._freq, key=self._freq.get)
        return None

    def on_access(self, cache_data: dict, key: str) -> None:
        self._freq[key] = self._freq.get(key, 0) + 1

    def on_add(self, cache_data: dict, key: str) -> None:
        self._freq[key] = 1

    def on_remove(self, cache_data: dict, key: str) -> None:
        self._freq.pop(key, None)

class OrderCache:
    """Кэш заказов, использующий стратегию вытеснения."""

    def __init__(self, strategy: EvictionStrategy, max_size: int = 100):
        self._max_size = max_size
        self._strategy = strategy
        self._data: dict = {}

    def is_cached(self, order_id: str) -> bool:
        if order_id in self._data:
            self._strategy.on_access(self._data, order_id)
            return True
        return False

    def add(self, order_id: str) -> None:
        evict_key = self._strategy.should_evict(self._data, self._max_size)

        if evict_key:
            del self._data[evict_key]
            self._strategy.on_remove(self._data, evict_key)
            print(f"Вытеснен заказ: {evict_key}")

        self._data[order_id] = True
        self._strategy.on_add(self._data, order_id)
        print(f"Order {order_id} добавлен в кэш (стратегия: {self._strategy.__class__.__name__})")

    def change_strategy(self, new_strategy: EvictionStrategy) -> None:
        """Меняет стратегию на лету с синхронизацией состояния."""
        for key in self._data.keys():
            new_strategy.on_add(self._data, key)

        self._strategy = new_strategy
        print(f"Стратегия изменена на: {new_strategy.__class__.__name__}")

    def __len__(self):
        return len(self._data)


class CacheManager:
    """Управляет созданием кэша и переключением стратегий."""

    @staticmethod
    def create_cache(strategy_name: str, max_size: int = 100, **kwargs) -> OrderCache:
        """Фабричный метод для создания кэша с нужной стратегией."""
        strategies = {
            'lru': LRUStrategy,
            'fifo': FIFOStrategy,
            'lfu': LFUStrategy
        }

        strategy_class = strategies.get(strategy_name.lower())
        if not strategy_class:
            raise ValueError(f"Неизвестная стратегия: {strategy_name}")


        strategy = strategy_class()

        return OrderCache(strategy, max_size)