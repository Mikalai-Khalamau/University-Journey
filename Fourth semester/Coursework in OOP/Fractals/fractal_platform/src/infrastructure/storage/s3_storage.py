from pathlib import Path

import numpy as np

from src.domain.interfaces.storage import IImageStorage


class S3ImageStorage(IImageStorage):
    """Stub adapter for future cloud storage migration."""

    def save(self, image: np.ndarray, filename: str) -> Path:
        raise NotImplementedError("S3 storage is not configured in educational mode")

    def delete(self, file_path: str) -> None:
        return None
