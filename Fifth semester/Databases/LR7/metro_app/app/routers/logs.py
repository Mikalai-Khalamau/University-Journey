from fastapi import APIRouter, Depends
import psycopg
from app.database import get_db

router = APIRouter(prefix="/logs", tags=["Журнал действий"])

@router.get("/")
def get_logs(limit: int = 50, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT al.id, al.timestamp, al.action_type, al.entity_name, al.entity_id, u.login as user_login
            FROM action_logs al
            LEFT JOIN system_users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
            LIMIT %s
        """, (limit,))
        return cur.fetchall()