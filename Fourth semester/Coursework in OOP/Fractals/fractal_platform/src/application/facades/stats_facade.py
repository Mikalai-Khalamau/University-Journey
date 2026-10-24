from uuid import UUID
from src.domain.interfaces.repository import IFractalRepository
from src.domain.value_objects.user_stats import UserStats

class StatsFacade:
    """
    Фасад, скрывающий сложные агрегирующие запросы к БД.
    Предоставляет единый интерфейс для получения статистики пользователя.
    """
    def __init__(self, repository: IFractalRepository) -> None:
        self.repository = repository

    def get_user_stats(self, user_id: UUID) -> UserStats:
        return self.repository.get_user_stats(user_id)