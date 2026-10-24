from __future__ import annotations

from src.core.config import AppConfig
from src.core.exceptions import ValidationError
from src.core.patterns.specification import ISpecification
from src.domain.value_objects.fractal_params import FractalParams


class ValidDimensionsSpec(ISpecification[FractalParams]):
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def is_satisfied_by(self, item: FractalParams) -> bool:
        return 0 < item.width <= self.config.max_width and 0 < item.height <= self.config.max_height


class ValidIterationsSpec(ISpecification[FractalParams]):
    def is_satisfied_by(self, item: FractalParams) -> bool:
        return 1 <= item.max_iter <= 10000


class FractalValidator:
    def __init__(self, config: AppConfig) -> None:
        self._specs: list[ISpecification[FractalParams]] = [ValidDimensionsSpec(config), ValidIterationsSpec()]

    def validate(self, params: FractalParams) -> None:
        for spec in self._specs:
            if not spec.is_satisfied_by(params):
                raise ValidationError(f"Validation failed: {spec.__class__.__name__}")
