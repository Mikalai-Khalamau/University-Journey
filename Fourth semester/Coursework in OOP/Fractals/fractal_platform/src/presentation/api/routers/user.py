from fastapi import APIRouter, Depends

from src.domain.entities.user import User
from src.presentation.api.dependencies import get_current_user, stats_facade

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/stats")
def get_user_stats(user: User = Depends(get_current_user)):
    """Получить статистику пользователя."""
    stats = stats_facade.get_user_stats(user.id)
    print(
        f"[Stats] User {user.id}: total={stats.total_generated}, fav={stats.favorite_type}, avg={stats.avg_generation_time_ms}ms")

    return {
        "total_generated": stats.total_generated,
        "favorite_type": stats.favorite_type,
        "avg_generation_time_ms": stats.avg_generation_time_ms,
        "total_time_ms": stats.total_time_ms
    }