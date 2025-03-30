from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import quote_plus

# Кодируем пароль для URL
encoded_password = quote_plus(settings.POSTGRES_PASSWORD)
database_url = f"postgresql://{settings.POSTGRES_USER}:{encoded_password}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 