from app.core.database import SessionLocal
from app.services.news_collector import NewsCollector
from app.models.news import Source

def collect_news():
    """
    Сбор новостей из всех активных источников
    """
    db = SessionLocal()
    try:
        # Получаем все активные источники
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        # Создаем коллектор новостей
        collector = NewsCollector(db)
        
        # Собираем новости из каждого источника
        for source in sources:
            print(f"Сбор новостей из {source.name}...")
            news_items = collector.collect_rss_feed(source)
            
            # Сохраняем новости в базу данных
            for news in news_items:
                db.add(news)
            
            db.commit()
            print(f"Собрано {len(news_items)} новостей из {source.name}")
        
        print("Сбор новостей завершен!")
        
    except Exception as e:
        print(f"Ошибка при сборе новостей: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    collect_news() 