from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import FractalPlatformError, UnauthorizedError


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(FractalPlatformError)
    async def handle_platform_error(_request: Request, exc: FractalPlatformError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedError)
    async def handle_unauthorized(_request: Request, exc: UnauthorizedError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(ValueError)
    async def handle_value_error(_request: Request, exc: ValueError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
