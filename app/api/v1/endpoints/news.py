from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.news import News, Source
from app.schemas.news import (
    News as NewsSchema,
    Source as SourceSchema,
    NewsStats
)
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=List[NewsSchema])
async def get_news(
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    source: Optional[str] = Query(None, description="Фильтр по источнику"),
    hours: Optional[int] = Query(None, description="Фильтр по времени (последние N часов)")
):
    """
    Получение списка новостей с фильтрацией и пагинацией
    
    Параметры:
    - page: номер страницы (по умолчанию 1)
    - category: фильтр по категории новостей
    - source: фильтр по источнику новостей
    - hours: фильтр по времени (показывает новости за последние N часов)
    """
    query = db.query(News)
    
    if category:
        query = query.filter(News.category == category)
    if source:
        query = query.join(Source).filter(Source.name == source)
    if hours:
        current_time = datetime.utcnow()
        time_threshold = current_time - timedelta(hours=hours)
        query = query.filter(
            and_(
                News.published_at >= time_threshold,
                News.published_at <= current_time
            )
        )
    
    # Пагинация
    per_page = 10
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    elif page > pages:
        page = pages
    
    news = query.order_by(desc(News.published_at)).offset((page - 1) * per_page).limit(per_page).all()
    return news

@router.get("/stats", response_model=NewsStats)
async def get_news_stats(db: Session = Depends(get_db)):
    """
    Получение статистики по новостям
    """
    # Общее количество новостей
    total_news = db.query(func.count(News.id)).scalar()
    
    # Количество новостей по категориям
    category_stats = db.query(
        News.category,
        func.count(News.id).label('count')
    ).group_by(News.category).all()
    
    # Количество новостей по источникам
    source_stats = db.query(
        Source.name,
        func.count(News.id).label('count')
    ).join(News).group_by(Source.name).all()
    
    # Количество новостей за последние 24 часа
    time_threshold = datetime.utcnow() - timedelta(hours=24)
    recent_news = db.query(func.count(News.id)).filter(
        News.published_at >= time_threshold
    ).scalar()
    
    return {
        "total_news": total_news,
        "by_category": {cat: count for cat, count in category_stats},
        "by_source": {source: count for source, count in source_stats},
        "last_24h": recent_news
    }

@router.get("/news/{news_id}", response_model=NewsSchema)
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news

@router.get("/sources/", response_model=List[SourceSchema])
def get_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()

@router.get("/sources/{source_id}", response_model=SourceSchema)
def get_source_by_id(source_id: int, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    return source

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """
    Получение списка всех категорий
    """
    categories = db.query(News.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]] 