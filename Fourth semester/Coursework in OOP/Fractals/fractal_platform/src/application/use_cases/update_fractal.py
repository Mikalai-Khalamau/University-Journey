from uuid import UUID

from src.core.exceptions import NotFoundError, ValidationError
from src.domain.interfaces.repository import IFractalRepository


class UpdateFractalUseCase:
    def __init__(self, repository: IFractalRepository) -> None:
        self.repository = repository

    def execute(self, fractal_id: UUID, user_id: UUID, name: str):
        name = name.strip()
        if not name:
            raise ValidationError("Name cannot be empty")
        fractal = self.repository.update_name(fractal_id, user_id, name)
        if fractal is None:
            raise NotFoundError("Fractal not found")
        return fractal
