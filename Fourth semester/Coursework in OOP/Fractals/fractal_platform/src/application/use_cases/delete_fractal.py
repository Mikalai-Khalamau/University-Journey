from uuid import UUID

from src.domain.interfaces.repository import IFractalRepository
from src.domain.interfaces.storage import IImageStorage


class DeleteFractalUseCase:
    def __init__(self, repository: IFractalRepository, storage: IImageStorage) -> None:
        self.repository = repository
        self.storage = storage

    def execute(self, fractal_id: UUID, user_id: UUID) -> bool:
        fractal = self.repository.get_by_id(fractal_id, user_id)
        if fractal:
            self.storage.delete(fractal.file_path)
        return self.repository.delete(fractal_id, user_id)
