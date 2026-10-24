from fastapi import APIRouter, Depends, HTTPException
import psycopg
from app.database import get_db
from app.models import IncidentCreate, IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Инциденты"])


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT i.id, i.description, i.status, i.created_at, 
                   eq.name as equipment_name, st.name as station_name, u.login as reporter
            FROM incidents i
            JOIN equipment eq ON i.equipment_id = eq.id
            JOIN stations st ON eq.station_id = st.id
            JOIN system_users u ON i.reported_id = u.id
            ORDER BY i.created_at DESC
        """)
        return cur.fetchall()


@router.post("/", response_model=dict)
def create_incident(incident: IncidentCreate, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id FROM equipment WHERE id = %s", (incident.equipment_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Оборудование не найдено")

        cur.execute("SELECT id FROM system_users WHERE id = %s", (incident.reported_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        cur.execute("""
            INSERT INTO incidents (equipment_id, reported_id, description, status) 
            VALUES (%s, %s, %s, 'open') RETURNING id
        """, (incident.equipment_id, incident.reported_id, incident.description))

        new_id = cur.fetchone()["id"]
        db.commit()

        cur.execute("SELECT log_action(%s, %s, %s, %s)",
                    (incident.reported_id, "insert", "incidents", new_id))
        db.commit()

        return {"message": "Инцидент создан", "id": new_id}


@router.put("/{incident_id}/status")
def update_incident_status(incident_id: int, new_status: str, user_id: int = 1,
                           db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("UPDATE incidents SET status = %s WHERE id = %s RETURNING id",
                    (new_status, incident_id))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Инцидент не найден")
        db.commit()

        cur.execute("SELECT log_action(%s, %s, %s, %s)", (user_id, "update", "incidents", incident_id))
        db.commit()

        return {"message": "Статус обновлён", "id": incident_id, "new_status": new_status}