from __future__ import annotations

import numpy as np

from src.domain.interfaces.processor import IImageProcessor


class WatermarkProcessor(IImageProcessor):
    def __init__(self, wrapped: IImageProcessor) -> None:
        self._wrapped = wrapped

    def process(self, image: np.ndarray) -> np.ndarray:
        image = self._wrapped.process(image)
        result = image.copy()
        result[-20:-5, -120:-5] = np.minimum(result[-20:-5, -120:-5] + 0.12, 1.0)
        return result
