class FractalPlatformError(Exception):
    """Base exception."""


class ValidationError(FractalPlatformError):
    """Input validation error."""


class NotFoundError(FractalPlatformError):
    """Entity not found."""


class GenerationError(FractalPlatformError):
    """Fractal generation error."""


class UnauthorizedError(FractalPlatformError):
    """Authentication required or invalid credentials."""
