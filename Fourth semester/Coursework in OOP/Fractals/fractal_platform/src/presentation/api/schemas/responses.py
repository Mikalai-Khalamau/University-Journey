from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str | None = None
    fractal_id: str | None = None


class FractalResponse(BaseModel):
    id: str
    created_at: str
    fractal_type: str
    params: dict
    file_path: str
    width: int
    height: int
    gamma: float
    generation_time_ms: float
