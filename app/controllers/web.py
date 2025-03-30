from fastapi import Request, Depends
from app.models.news import News, Source
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

async def get_news_page(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    category: Optional[str] = None,
    source_id: Optional[int] = None
):
    """
    Получение данных для страницы новостей
    """
    # Базовый запрос
    query = db.query(News)
    
    # Применяем фильтры
    if category:
        query = query.filter(News.category == category)
    if source_id:
        query = query.filter(News.source_id == source_id)
    
    # Получаем общее количество новостей
    total_news = query.count()
    
    # Получаем новости для текущей страницы
    news = query.order_by(desc(News.published_at))\
        .offset((page - 1) * 10)\
        .limit(10)\
        .all()
    
    # Получаем список источников для фильтра
    sources = db.query(Source).all()
    
    # Получаем список категорий для фильтра
    categories = db.query(News.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return {
        "request": request,
        "news": news,
        "sources": sources,
        "categories": categories,
        "current_page": page,
        "total_pages": (total_news + 9) // 10,
        "selected_category": category,
        "selected_source": source_id
    }

async def get_sources_page(request: Request, db: Session = Depends(get_db)):
    """
    Получение данных для страницы управления источниками
    """
    sources = db.query(Source).all()
    return {
        "request": request,
        "sources": sources
    } 