# Fractal Platform

Web-platform for fractal generation and collection management.

## Features

- Mandelbrot and IFS flame-like generation
- Async background generation with task status tracking
- PNG storage with normalization and gamma correction
- SQLite + SQLAlchemy metadata storage
- REST API with OpenAPI docs at `/docs`
- Import/export of generation parameters JSON

## Run

```bash
pip install -e .[dev]
uvicorn src.main:app --reload
```

Open UI: `http://127.0.0.1:8000/`
Open API docs: `http://127.0.0.1:8000/docs`

## Main Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/fractals/generate`
- `GET /api/fractals`
- `GET /api/fractals/{fractal_id}`
- `PUT /api/fractals/{fractal_id}`
- `DELETE /api/fractals/{fractal_id}`
- `GET /api/tasks/{task_id}`
- `GET /api/fractals/{fractal_id}/export`
- `POST /api/fractals/import`
