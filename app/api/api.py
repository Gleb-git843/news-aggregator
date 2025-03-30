from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.news import Source as SourceModel, News as NewsModel
from app.schemas.news import Source as SourceSchema, SourceCreate, SourceUpdate, News as NewsSchema
from typing import List, Optional
from sqlalchemy import desc

api_router = APIRouter()

@api_router.get("/news", response_model=List[NewsSchema])
async def get_news(
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    source_id: Optional[int] = Query(None, description="Фильтр по источнику")
):
    """
    Получение списка новостей с фильтрацией и пагинацией
    """
    query = db.query(NewsModel)
    
    if category:
        query = query.filter(NewsModel.category == category)
    if source_id:
        query = query.filter(NewsModel.source_id == source_id)
    
    # Пагинация
    per_page = 10
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    elif page > pages:
        page = pages
    
    news = query.order_by(desc(NewsModel.published_at)).offset((page - 1) * per_page).limit(per_page).all()
    return news

@api_router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """
    Получение списка всех категорий
    """
    categories = db.query(NewsModel.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@api_router.get("/sources", response_model=List[SourceSchema])
async def get_sources(db: Session = Depends(get_db)):
    """
    Получение списка всех источников
    """
    return db.query(SourceModel).all()

@api_router.post("/sources", response_model=SourceSchema)
async def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """
    Создание нового источника
    """
    db_source = SourceModel(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@api_router.get("/sources/{source_id}", response_model=SourceSchema)
async def get_source(source_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о конкретном источнике
    """
    source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    return source

@api_router.put("/sources/{source_id}", response_model=SourceSchema)
async def update_source(source_id: int, source: SourceUpdate, db: Session = Depends(get_db)):
    """
    Обновление информации об источнике
    """
    db_source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    for key, value in source.dict(exclude_unset=True).items():
        setattr(db_source, key, value)
    
    db.commit()
    db.refresh(db_source)
    return db_source

@api_router.delete("/sources/{source_id}")
async def delete_source(source_id: int, db: Session = Depends(get_db)):
    """
    Удаление источника
    """
    db_source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    db.delete(db_source)
    db.commit()
    return {"message": "Источник успешно удален"} 