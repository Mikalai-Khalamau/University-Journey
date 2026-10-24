from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from clients.database import init_db
from shared.exceptions import BaseAppError, NotFoundError, BusinessRuleError, AuthError

init_db()

app = FastAPI(
    title="Food Delivery Backend",
    description="Система управления доставкой еды",
    docs_url="/docs",
    redoc_url="/redoc",
openapi_tags=[
        {"name": "Auth", "description": "Регистрация и аутентификация пользователей"},
        {"name": "Menu", "description": "Просмотр и добавление блюд в меню"},
        {"name": "Orders", "description": "Управление заказами, статусами и курьерами"},
        {"name": "Couriers", "description": "Управление курьерами"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

@app.exception_handler(BusinessRuleError)
async def business_rule_handler(request: Request, exc: BusinessRuleError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

@app.exception_handler(AuthError)
async def auth_handler(request: Request, exc: AuthError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})

@app.exception_handler(BaseAppError)
async def base_app_handler(request: Request, exc: BaseAppError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

app.include_router(api_router, prefix="/api/v1", tags=["Food Delivery"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)