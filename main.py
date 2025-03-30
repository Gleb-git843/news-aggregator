from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.api import api_router
from app.core.config import settings
from typing import Optional
from pathlib import Path

app = FastAPI(
    title="News Aggregator API",
    description="API для агрегации новостей",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на список разрешенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутеры
app.include_router(api_router, prefix="/api")

@app.get("/")
async def home(
    request: Request,
    page: int = Query(1, description="Номер страницы"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    source_id: Optional[int] = Query(None, description="Фильтр по источнику")
):
    """
    Главная страница с новостями
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "page": page, "category": category, "source_id": source_id}
    )

@app.get("/sources")
async def sources_page(request: Request):
    """
    Страница управления источниками
    """
    return templates.TemplateResponse("sources.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 