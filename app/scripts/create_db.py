from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models.news import Base, News, Source

def create_database():
    # Создаем подключение к postgres для создания базы данных
    engine = create_engine(
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/postgres"
    )
    
    # Проверяем существование базы данных
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'"))
        if not result.scalar():
            # Создаем базу данных, если она не существует
            conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))
            print(f"База данных {settings.POSTGRES_DB} успешно создана")
        else:
            print(f"База данных {settings.POSTGRES_DB} уже существует")

def create_tables():
    # Создаем подключение к нашей базе данных
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        exit(1) 