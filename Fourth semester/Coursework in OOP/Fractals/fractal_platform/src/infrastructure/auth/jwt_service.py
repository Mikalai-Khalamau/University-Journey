from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from src.core.config import AppConfig
from src.core.exceptions import ValidationError


class JwtService:
    def __init__(self, config: AppConfig) -> None:
        self._secret = config.jwt_secret
        self._algorithm = "HS256"
        self._expire_minutes = config.jwt_expire_minutes

    def create_token(self, user_id: UUID, username: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": str(user_id), "username": username, "exp": expire}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except JWTError as exc:
            raise ValidationError("Invalid or expired token") from exc
