class BaseAppError(Exception):
    """Базовое исключение приложения."""
    pass

class NotFoundError(BaseAppError):
    """Запрашиваемый ресурс не найден."""
    pass

class BusinessRuleError(BaseAppError):
    """Нарушено бизнес-правило."""
    pass

class AuthError(BaseAppError):
    """Ошибка аутентификации/авторизации."""
    pass