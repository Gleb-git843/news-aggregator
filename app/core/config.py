from typing import Optional
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "News Aggregator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Настройки базы данных
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Val@2910P"
    POSTGRES_DB: str = "news_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # Настройки Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-here"
    
    # Настройки для сбора новостей
    NEWS_COLLECTION_INTERVAL: int = 3600  # 1 час в секундах
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            # Кодируем специальные символы в пароле
            encoded_password = quote_plus(self.POSTGRES_PASSWORD)
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{encoded_password}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = Settings() 