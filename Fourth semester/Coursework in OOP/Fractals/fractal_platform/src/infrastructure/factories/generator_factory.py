from __future__ import annotations

from src.core.exceptions import ValidationError
from src.domain.interfaces.generator import IFractalGenerator
from src.infrastructure.generators.burning_ship import BurningShipGenerator
from src.infrastructure.generators.ifs import IFSFractalGenerator
from src.infrastructure.generators.julia import JuliaGenerator
from src.infrastructure.generators.mandelbrot import MandelbrotGenerator


class FractalGeneratorFactory:
    def create(self, fractal_type: str) -> IFractalGenerator:
        mapping = {
            "mandelbrot": MandelbrotGenerator,
            "julia": JuliaGenerator,
            "ifs": IFSFractalGenerator,
            "burning_ship": BurningShipGenerator,
        }
        if fractal_type not in mapping:
            raise ValidationError(f"Unsupported fractal type: {fractal_type}")
        return mapping[fractal_type]()
