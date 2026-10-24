from __future__ import annotations

import numpy as np
from src.domain.interfaces.processor import IImageProcessor


class BaseImageProcessor(IImageProcessor):
    def process(self, image: np.ndarray) -> np.ndarray:
        return image


class NormalizationProcessor(IImageProcessor):
    def __init__(self, wrapped: IImageProcessor | None = None) -> None:
        self._wrapped = wrapped or BaseImageProcessor()

    def process(self, image: np.ndarray) -> np.ndarray:
        """Безопасная нормализация для [0,1] изображений"""
        image = self._wrapped.process(image)
        return np.clip(image, 0.0, 1.0)