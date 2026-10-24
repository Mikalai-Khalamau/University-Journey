from dataclasses import dataclass

@dataclass
class UserStats:
    total_generated: int = 0
    favorite_type: str | None = None
    avg_generation_time_ms: float = 0.0
    total_time_ms: float = 0.0