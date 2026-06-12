from fastapi import APIRouter

# Створюємо роутер
router = APIRouter(prefix="/ping", tags=["ping"])

# Маршрут для перевірки бази даних
@router.get("/db")
async def ping_db():
    return {"message": "ok"}

# Маршрут для перевірки роботи додатку
@router.get("/app")
async def ping_app():
    return {"text": "app is working"}