from dataclasses import dataclass


@dataclass(frozen=True)
class ImageMetadata:
    width: int
    height: int
    color_mode: str = "RGB"
    gamma: float = 2.2
    file_size: int | None = None
