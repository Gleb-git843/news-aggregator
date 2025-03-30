from app.db.session import SessionLocal
from app.models.news import NewsSource

def add_initial_sources():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже источники
        existing_sources = db.query(NewsSource).count()
        if existing_sources > 0:
            print("Источники уже существуют")
            return

        # Создаем начальные источники
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
            NewsSource(
                name="Интерфакс",
                url="https://www.interfax.ru/rss.asp",
                description="Интерфакс - информационное агентство",
                type="RSS"
            ),
            NewsSource(
                name="Lenta.ru",
                url="https://lenta.ru/rss",
                description="Новости Lenta.ru",
                type="RSS"
            )
        ]
        
        for source in sources:
            db.add(source)
        
        db.commit()
        print("Начальные источники успешно добавлены")
    except Exception as e:
        print(f"Ошибка при добавлении источников: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_initial_sources() 