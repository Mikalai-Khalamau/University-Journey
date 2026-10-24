from fastapi import FastAPI
from app.routers import auth, users, stations, trains, incidents, logs

app = FastAPI(
    title="Система учета Метрополитена",
    description="API для управления инфраструктурой метрополитена",
    version="2.0.0"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(stations.router)
app.include_router(trains.router)
app.include_router(incidents.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {"message": "Система учета Метрополитена API", "docs": "/docs"}