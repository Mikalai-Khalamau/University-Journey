from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class IImageStorage(ABC):
    @abstractmethod
    def save(self, image: np.ndarray, filename: str) -> Path:
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> None:
        raise NotImplementedError
