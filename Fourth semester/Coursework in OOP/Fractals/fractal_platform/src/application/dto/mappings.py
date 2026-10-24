from src.domain.entities.fractal import Fractal


def fractal_to_dict(fractal: Fractal) -> dict:
    return {
        "id": str(fractal.id),
        "name": fractal.name,
        "created_at": fractal.created_at.isoformat(),
        "fractal_type": fractal.fractal_type,
        "params": fractal.params.to_dict(),
        "file_path": fractal.file_path,
        "width": fractal.metadata.width,
        "height": fractal.metadata.height,
        "gamma": fractal.metadata.gamma,
        "generation_time_ms": fractal.generation_time_ms,
        "image_url": f"/api/fractals/{fractal.id}/image",
        "tags": fractal.tags if fractal.tags else ["basic"],
    }