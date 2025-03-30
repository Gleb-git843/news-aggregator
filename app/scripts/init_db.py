import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import Base, engine
from app.models.news import Source, News

def init_db():
    """
    Инициализация базы данных
    """
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Создание таблиц базы данных...")
    init_db()
    print("Таблицы успешно созданы!") 