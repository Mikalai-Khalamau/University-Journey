from fastapi import APIRouter, Depends, HTTPException
import psycopg
from app.database import get_db
from app.models import UserLogin, UserResponse
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/login")
def login(user: UserLogin, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, login, role, password_hash FROM system_users WHERE login = %s",
            (user.login,)
        )
        db_user = cur.fetchone()

    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    with db.cursor() as cur:
        cur.execute("SELECT log_action(%s, %s, %s, %s)",
                    (db_user["id"], "login", "system_users", db_user["id"]))
        db.commit()

    return {"message": "Успешный вход", "user": UserResponse(**db_user)}