import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.presentation.api.routers.auth import router as auth_router
from src.presentation.api.routers.fractals import router as fractals_router
from src.presentation.api.routers.tasks import router as tasks_router
from src.presentation.api.routers.user import router as user_router
from src.presentation.exceptions_handler import add_exception_handlers

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Fractal Platform", version="0.1.0")
add_exception_handlers(app)
base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(base_dir / "presentation" / "web" / "static")), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def index(_request: Request):
    return FileResponse(str(base_dir / "presentation" / "web" / "templates" / "index.html"))

app.include_router(user_router, prefix="/api")
app.include_router(fractals_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(auth_router, prefix="/api")