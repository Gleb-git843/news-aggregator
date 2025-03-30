from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.news import News, Source
from app.schemas.news import (
    News as NewsSchema,
    NewsCreate,
    Source as SourceSchema,
    SourceCreate,
    SourceUpdate
)
from sqlalchemy import desc

router = APIRouter()

@router.get("/", response_model=List[NewsSchema])
async def get_news(
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    source_id: Optional[int] = Query(None, description="Фильтр по источнику")
):
    """
    Получение списка новостей с фильтрацией и пагинацией
    """
    query = db.query(News)
    
    if category:
        query = query.filter(News.category == category)
    if source_id:
        query = query.filter(News.source_id == source_id)
    
    # Пагинация
    per_page = 10
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    elif page > pages:
        page = pages
    
    news = query.offset((page - 1) * per_page).limit(per_page).all()
    return news

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """
    Получение списка всех категорий
    """
    categories = db.query(News.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@router.get("/sources", response_model=List[SourceSchema])
async def get_sources(
    db: Session = Depends(get_db),
    active_only: bool = Query(True, description="Только активные источники")
):
    """
    Получение списка источников новостей
    """
    query = db.query(Source)
    if active_only:
        query = query.filter(Source.is_active == True)
    sources = query.all()
    return sources

@router.post("/sources", response_model=SourceSchema)
async def create_source(
    source: SourceCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового источника новостей
    """
    db_source = Source(**source.dict())
    db.add(db_source)
    try:
        db.commit()
        db.refresh(db_source)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_source

@router.put("/sources/{source_id}", response_model=SourceSchema)
async def update_source(
    source_id: int,
    source_update: SourceUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновление существующего источника новостей
    """
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    for field, value in source_update.dict(exclude_unset=True).items():
        setattr(db_source, field, value)
    
    try:
        db.commit()
        db.refresh(db_source)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_source

@router.delete("/sources/{source_id}")
async def delete_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаление источника новостей
    """
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    try:
        db.delete(db_source)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Источник успешно удален"} 