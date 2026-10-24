from __future__ import annotations
import re
from uuid import UUID
from src.core.exceptions import UnauthorizedError, ValidationError
from src.domain.entities.user import User
from src.domain.interfaces.user_repository import IUserRepository
from src.infrastructure.auth.jwt_service import JwtService
from src.infrastructure.auth.password import hash_password, verify_password


class AuthService:
    def __init__(self, user_repository: IUserRepository, jwt_service: JwtService):
        self._users = user_repository
        self._jwt = jwt_service

    @staticmethod
    def validate_password(password: str, confirm: str) -> None:
        """Проверяет пароль: 4+ символов, буква, цифра, спецсимвол, совпадение"""
        if len(password) < 4:
            raise ValidationError("Пароль должен быть минимум 4 символа")
        if password != confirm:
            raise ValidationError("Пароли не совпадают")
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну латинскую букву")
        if not re.search(r'\d', password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r'[^A-Za-z\d]', password):
            raise ValidationError("Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*)")

    def register(self, username: str, password: str, email: str = None, confirm_password: str = None) -> User:
        username = username.strip()
        if len(username) < 3:
            raise ValidationError("Логин должен быть минимум 3 символа")

        self.validate_password(password, confirm_password)

        if self._users.get_by_username(username):
            raise ValidationError("Пользователь уже существует")

        user = User(username=username, password_hash=hash_password(password), email=email)
        return self._users.save(user)

    def login(self, username: str, password: str) -> tuple[str, User]:
        user = self._users.get_by_username(username.strip())
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверный логин или пароль")
        token = self._jwt.create_token(user.id, user.username)
        return token, user

    def get_user_from_token(self, token: str) -> User:
        payload = self._jwt.decode_token(token)
        user = self._users.get_by_id(UUID(payload["sub"]))
        if not user:
            raise UnauthorizedError("Пользователь не найден")
        return user