from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from pydantic import Field

@dataclass(frozen=True)
class AppConfig:
    database_url: str
    media_dir: Path
    max_width: int
    max_height: int
    default_gamma: float
    jwt_secret: str
    jwt_expire_minutes: int
    smtp_host: str = Field(default="localhost")
    smtp_port: int = Field(default=25)
    smtp_use_tls: bool = Field(default=False)
    email_from: str = Field(default="noreply@fractal.platform")


class ConfigLoader:
    _instance: "ConfigLoader | None" = None
    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_use_tls: bool = False
    email_from: str = "noreply@fractal.platform"

    def __new__(cls) -> "ConfigLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @lru_cache(maxsize=1)
    def load(self) -> AppConfig:
        media_dir = Path(os.getenv("FRACTAL_MEDIA_DIR", "media")).resolve()
        media_dir.mkdir(parents=True, exist_ok=True)
        return AppConfig(
            database_url=os.getenv("FRACTAL_DB_URL", "sqlite:///fractal_platform.db"),
            media_dir=media_dir,
            max_width=int(os.getenv("FRACTAL_MAX_WIDTH", "4096")),
            max_height=int(os.getenv("FRACTAL_MAX_HEIGHT", "4096")),
            default_gamma=float(os.getenv("FRACTAL_DEFAULT_GAMMA", "2.2")),
            jwt_secret=os.getenv("FRACTAL_JWT_SECRET", "change-me-in-production"),
            jwt_expire_minutes=int(os.getenv("FRACTAL_JWT_EXPIRE_MINUTES", "10080")),
        )
