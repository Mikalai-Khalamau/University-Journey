from __future__ import annotations

import numpy as np
from src.domain.interfaces.processor import IImageProcessor


class GammaCorrectionProcessor(IImageProcessor):
    def __init__(self, gamma: float, wrapped: IImageProcessor | None = None) -> None:
        self.gamma = gamma if gamma > 0 else 2.2
        self._wrapped = wrapped

    def process(self, image: np.ndarray) -> np.ndarray:
        if self._wrapped is not None:
            image = self._wrapped.process(image)

        image = np.clip(image, 0.0, 1.0)

        return np.power(image, 1.0 / self.gamma)