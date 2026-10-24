from fastapi import APIRouter, Depends
import psycopg
from app.database import get_db
from app.models import TrainResponse

router = APIRouter(prefix="/trains", tags=["Поезда"])

@router.get("/", response_model=list[TrainResponse])
def get_trains(db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT t.id, t.number, t.model, t.status, l.name as line_name
            FROM trains t
            JOIN lines l ON t.line_id = l.id
            ORDER BY l.name, t.number
        """)
        return cur.fetchall()