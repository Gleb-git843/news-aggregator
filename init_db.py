from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models.base import Base

def init_database():
    # Создаем движок для подключения к PostgreSQL
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Создаем базу данных, если она не существует
    with engine.connect() as conn:
        conn.execute(text("commit"))
        try:
            conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))
            print(f"База данных {settings.POSTGRES_DB} успешно создана")
        except Exception as e:
            print(f"База данных {settings.POSTGRES_DB} уже существует или произошла ошибка: {e}")
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы")

if __name__ == "__main__":
    init_database() 