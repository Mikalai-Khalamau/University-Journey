from uuid import UUID

from src.application.use_cases.generate_fractal import GenerateFractalUseCase
from src.domain.value_objects.fractal_params import build_fractal_params


class ImportParamsUseCase:
    def __init__(self, generate_use_case: GenerateFractalUseCase) -> None:
        self.generate_use_case = generate_use_case

    def execute(self, data: dict, user_id: UUID, name: str):
        params = build_fractal_params(data)
        return self.generate_use_case.execute(params, user_id, name)
