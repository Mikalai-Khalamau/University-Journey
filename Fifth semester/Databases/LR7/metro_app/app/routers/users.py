from fastapi import APIRouter, Depends, HTTPException
import psycopg
from app.database import get_db
from app.models import UserCreate, UserResponse
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/", response_model=list[UserResponse])
def get_users(db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, login, role, created_at FROM system_users ORDER BY id")
        return cur.fetchall()


@router.post("/", response_model=UserResponse)
def create_user(new_user: UserCreate, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        hashed = hash_password(new_user.password)
        cur.execute(
            "INSERT INTO system_users (login, password_hash, role) VALUES (%s, %s, %s) RETURNING id, login, role",
            (new_user.login, hashed, new_user.role)
        )
        created = cur.fetchone()
        db.commit()

        cur.execute("SELECT log_action(%s, %s, %s, %s)",
                    (created["id"], "insert", "system_users", created["id"]))
        db.commit()

        return created


@router.delete("/{user_id}")
def delete_user(user_id: int, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM system_users WHERE id = %s RETURNING id", (user_id,))
        deleted = cur.fetchone()
        if not deleted:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        db.commit()

        cur.execute("SELECT log_action(%s, %s, %s, %s)", (user_id, "delete", "system_users", user_id))
        db.commit()
        return {"message": "Пользователь удален"}