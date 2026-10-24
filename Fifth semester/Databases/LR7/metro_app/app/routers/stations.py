from fastapi import APIRouter, Depends
import psycopg
from app.database import get_db
from app.models import StationResponse

router = APIRouter(prefix="/stations", tags=["Станции"])

@router.get("/", response_model=list[StationResponse])
def get_stations(db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT s.id, s.name, s.depth, l.name as line_name 
            FROM stations s 
            JOIN lines l ON s.line_id = l.id
            ORDER BY l.name, s.name
        """)
        return cur.fetchall()