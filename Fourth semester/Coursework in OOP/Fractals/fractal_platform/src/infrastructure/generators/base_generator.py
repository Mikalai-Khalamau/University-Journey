from __future__ import annotations

from abc import abstractmethod
import numpy as np

from src.domain.interfaces.generator import IFractalGenerator
from src.domain.value_objects.fractal_params import FractalParams


class BaseFractalGenerator(IFractalGenerator):
    def generate(self, params: FractalParams) -> np.ndarray:
        self._validate(params)
        values = self._compute(params)
        rgb = self._to_rgb(values)
        return rgb

    def _validate(self, params: FractalParams) -> None:
        if params.width <= 0 or params.height <= 0:
            raise ValueError("Invalid dimensions")

    @abstractmethod
    def _compute(self, params: FractalParams) -> np.ndarray:
        raise NotImplementedError

    def _to_rgb(self, values: np.ndarray) -> np.ndarray:
        if values.ndim == 2:
            max_iter = int(values.max())
            if max_iter == 0:
                return np.zeros((values.shape[0], values.shape[1], 3), dtype=np.float64)

            interior = values >= max_iter
            norm = np.where(interior, 0.0, np.log1p(values) / np.log1p(max_iter))

            r = 0.5 * (1 + np.cos(2 * np.pi * (norm * 4.0 + 0.00)))
            g = 0.5 * (1 + np.cos(2 * np.pi * (norm * 4.0 + 0.33)))
            b = 0.5 * (1 + np.cos(2 * np.pi * (norm * 4.0 + 0.67)))

            r[interior] = 0.0
            g[interior] = 0.0
            b[interior] = 0.0

            return np.stack([r, g, b], axis=-1)
        else:
            return values.astype(np.float64) / 255.0