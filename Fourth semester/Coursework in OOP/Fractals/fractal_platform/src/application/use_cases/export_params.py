import json
from uuid import UUID

from src.core.exceptions import NotFoundError
from src.domain.interfaces.repository import IFractalRepository


class ExportParamsUseCase:
    def __init__(self, repository: IFractalRepository) -> None:
        self.repository = repository

    def execute(self, fractal_id: UUID, user_id: UUID) -> str:
        fractal = self.repository.get_by_id(fractal_id, user_id)
        if fractal is None:
            raise NotFoundError("Fractal not found")
        return json.dumps(fractal.params.to_dict(), ensure_ascii=False, indent=2)
