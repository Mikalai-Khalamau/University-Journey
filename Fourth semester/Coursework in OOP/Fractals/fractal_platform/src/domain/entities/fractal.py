from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.value_objects.fractal_params import FractalParams
from src.domain.value_objects.image_metadata import ImageMetadata


@dataclass
class Fractal:
    user_id: UUID
    name: str
    fractal_type: str
    params: FractalParams
    metadata: ImageMetadata
    file_path: str
    generation_time_ms: float
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list[str] = field(default_factory=lambda: ["basic"])