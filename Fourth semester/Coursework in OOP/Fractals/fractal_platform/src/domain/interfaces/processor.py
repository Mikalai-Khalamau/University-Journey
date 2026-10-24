from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class IImageProcessor(ABC):
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError
