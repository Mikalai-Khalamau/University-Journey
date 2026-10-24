from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image
from src.domain.interfaces.storage import IImageStorage


class FileImageStorage(IImageStorage):
    def __init__(self, media_dir: Path) -> None:
        self.media_dir = media_dir
        self.media_dir.mkdir(parents=True, exist_ok=True)

    def save(self, image: np.ndarray, filename: str) -> Path:
        file_path = self.media_dir / filename
        print(
            f"[3] Перед сохранением: min={image.min():.4f}, max={image.max():.4f}, dtype={image.dtype}, ndim={image.ndim}")

        # Безопасная конвертация в uint8 [0, 255]
        if image.dtype != np.uint8:
            # Если float [0, 1], то масштабируем к [0, 255]
            if np.issubdtype(image.dtype, np.floating):
                image = np.clip(image * 255.0, 0, 255)
            image = image.astype(np.uint8)

        if image.ndim == 2:
            image = np.stack([image] * 3, axis=-1)
        elif image.ndim == 3 and image.shape[2] == 1:
            image = np.repeat(image, 3, axis=2)

        print(f"[4] Финальный массив: min={image.min()}, max={image.max()}, dtype={image.dtype}")
        img = Image.fromarray(image, mode="RGB")
        img.save(file_path, format="PNG")
        return file_path

    def delete(self, file_path: str) -> None:
        path = Path(file_path)
        if path.exists():
            path.unlink()