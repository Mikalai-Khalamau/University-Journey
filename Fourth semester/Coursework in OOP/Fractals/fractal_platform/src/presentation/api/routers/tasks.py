from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.domain.entities.user import User
from src.presentation.api.dependencies import task_tracker, ui_notifier, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}")
def get_task(task_id: UUID, user: User = Depends(get_current_user)):
    data = task_tracker.get(task_id, user.id)
    if data is None:
        raise HTTPException(status_code=404, detail="Task not found")

    pending = ui_notifier.get_pending(str(user.id))

    return {
        "task_id": str(task_id),
        "status": data["status"],
        "message": data.get("message"),
        "fractal_id": data.get("fractal_id"),
        "has_notifications": len(pending) > 0,
        "notifications": pending,
    }