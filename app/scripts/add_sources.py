import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.models.news import Source

def add_initial_sources():
    """
    Добавление начальных источников новостей
    """
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже источники
        if db.query(Source).count() > 0:
            print("Источники уже существуют в базе данных.")
            return

        # Список начальных источников
        sources = [
            {
                "name": "РИА Новости",
                "url": "https://ria.ru/export/rss2/archive/index.xml",
                "is_active": True
            },
            {
                "name": "ТАСС",
                "url": "https://tass.ru/rss/v2.xml",
                "is_active": True
            },
            {
                "name": "Интерфакс",
                "url": "https://www.interfax.ru/rss.asp",
                "is_active": True
            },
            {
                "name": "Lenta.ru",
                "url": "https://lenta.ru/rss",
                "is_active": True
            },
            {
                "name": "РБК",
                "url": "https://www.rbc.ru/rss/main.rss",
                "is_active": True
            }
        ]

        # Добавляем источники
        for source_data in sources:
            source = Source(**source_data)
            db.add(source)
        
        db.commit()
        print("Начальные источники успешно добавлены!")
        
    except Exception as e:
        print(f"Ошибка при добавлении источников: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Добавление начальных источников...")
    add_initial_sources() 