from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from src.domain.value_objects.fractal_params import FractalParams


class IFractalGenerator(ABC):
    @abstractmethod
    def generate(self, params: FractalParams) -> np.ndarray:
        raise NotImplementedError
