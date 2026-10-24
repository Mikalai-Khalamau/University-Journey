from uuid import UUID

from src.domain.interfaces.repository import IFractalRepository
from src.domain.entities.fractal import Fractal

class GetFractalCollectionUseCase:
    def __init__(self, repository: IFractalRepository) -> None:
        self.repository = repository

    def execute(self, user_id: UUID):
        return self.repository.list_by_user(user_id)

    def execute_all(self) -> list[Fractal]:
        """Возвращает все фракталы (для публичного доступа к изображениям)"""
        return self.repository.list_all()
