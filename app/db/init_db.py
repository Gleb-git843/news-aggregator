from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.base import Base
from app.db.session import engine

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы")

def create_initial_sources(db: Session):
    """Создание начальных источников новостей"""
    from app.models.news import NewsSource
    
    sources = [
        NewsSource(
            name="РИА Новости",
            url="https://ria.ru/export/rss2/archive/index.xml",
            description="Российское информационное агентство",
            type="RSS"
        ),
        NewsSource(
            name="ТАСС",
            url="https://tass.ru/rss/v2.xml",
            description="Телеграфное агентство Советского Союза",
            type="RSS"
        ),
        # Добавьте другие источники по необходимости
    ]
    
    for source in sources:
        db.add(source)
    
    db.commit() 