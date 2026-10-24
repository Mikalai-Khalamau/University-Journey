from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.application.dto.mappings import fractal_to_dict
from src.domain.entities.user import User
from src.domain.value_objects.fractal_params import build_fractal_params
from src.presentation.api.dependencies import (
    collection_use_case,
    delete_use_case,
    export_use_case,
    get_current_user,
    import_use_case,
    task_tracker,
    update_use_case,
    worker,
)
from src.presentation.api.schemas.requests import (
    GenerateRequest,
    ImportRequest,
    UpdateFractalRequest,
    UpdateTagsRequest,
)

router = APIRouter(prefix="/fractals", tags=["fractals"])


@router.post("/generate")
def generate(request: GenerateRequest, user: User = Depends(get_current_user)):
    import json
    print(f"[API] Raw request body: {json.dumps(request.model_dump(), indent=2)}")

    task_id = uuid4()
    task_tracker.create(task_id, user.id)
    params_data = request.model_dump(exclude_none=True)

    from datetime import datetime
    name = params_data.pop("name", None)
    tags = params_data.pop("tags", ["basic"])

    if not name:
        short_hash = uuid4().hex[:6]
        timestamp = datetime.now().strftime("%H%M")
        name = f"{request.fractal_type.title()} #{short_hash} {timestamp}"

    worker.submit(
        task_id,
        {
            "params": build_fractal_params(params_data),
            "user_id": user.id,
            "name": name,
            "tags": tags,
        },
    )
    return {"task_id": str(task_id), "status": "pending"}


@router.get("/tags")
def list_tags(user: User = Depends(get_current_user)):
    """Возвращает все уникальные теги пользователя."""
    from src.presentation.api.dependencies import repository
    return {"tags": repository.list_user_tags(user.id)}


@router.get("")
def list_fractals(user: User = Depends(get_current_user)):
    fractals = collection_use_case.execute(user.id)
    return [fractal_to_dict(item) for item in fractals]


@router.get("/{fractal_id}")
def get_fractal(fractal_id: UUID, user: User = Depends(get_current_user)):
    for fractal in collection_use_case.execute(user.id):
        if fractal.id == fractal_id:
            return fractal_to_dict(fractal)
    raise HTTPException(status_code=404, detail="Fractal not found")


@router.get("/{fractal_id}/image")
def get_fractal_image(fractal_id: UUID):
    from pathlib import Path
    from src.presentation.api.dependencies import repository

    fractal = repository.get_by_id_raw(fractal_id)
    if fractal is None:
        raise HTTPException(status_code=404, detail="Fractal not found")

    abs_path = Path(fractal.file_path).resolve()
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(str(abs_path), media_type="image/png")


@router.put("/{fractal_id}")
def update(fractal_id: UUID, request: UpdateFractalRequest, user: User = Depends(get_current_user)):
    fractal = update_use_case.execute(fractal_id, user.id, request.name)
    return fractal_to_dict(fractal)


@router.put("/{fractal_id}/tags")
def update_tags(fractal_id: UUID, request: UpdateTagsRequest, user: User = Depends(get_current_user)):
    """Обновляет теги фрактала."""
    from src.presentation.api.dependencies import repository
    fractal = repository.update_tags(fractal_id, user.id, request.tags)
    if not fractal:
        raise HTTPException(status_code=404, detail="Fractal not found")
    return fractal_to_dict(fractal)


@router.delete("/{fractal_id}")
def delete(fractal_id: UUID, user: User = Depends(get_current_user)):
    deleted = delete_use_case.execute(fractal_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fractal not found")
    return {"deleted": True}


@router.get("/{fractal_id}/export")
def export(fractal_id: UUID, user: User = Depends(get_current_user)):
    return {"params_json": export_use_case.execute(fractal_id, user.id)}


@router.post("/import")
def import_params(request: ImportRequest, user: User = Depends(get_current_user)):
    fractal_id = import_use_case.execute(
        request.params,
        user.id,
        request.name or "Imported fractal",
    )
    return {"fractal_id": str(fractal_id)}


@router.get("/collection", include_in_schema=False)
def collection_page():
    from pathlib import Path

    presentation_dir = Path(__file__).resolve().parent.parent.parent
    collection_file = presentation_dir / "web" / "templates" / "collection.html"

    if not collection_file.exists():
        raise HTTPException(status_code=500, detail=f"Template not found: {collection_file}")

    return FileResponse(str(collection_file))