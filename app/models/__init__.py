from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

# Создаем движок SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

# Импортируем модели после создания Base
from app.models.news import News, Source

# Экспортируем все необходимые компоненты
__all__ = ['Base', 'engine', 'SessionLocal', 'News', 'Source']
