from app.db.session import SessionLocal
from app.models.news import NewsSource
from app.services.news_collector import NewsCollector

def test_news_collection():
    db = SessionLocal()
    try:
        # Получаем все источники
        sources = db.query(NewsSource).all()
        collector = NewsCollector(db)
        
        for source in sources:
            print(f"\nСбор новостей из источника: {source.name}")
            
            if source.type == "RSS":
                news_items = collector.collect_rss_feed(source)
            else:
                news_items = collector.collect_website(source)
            
            print(f"Найдено новостей: {len(news_items)}")
            collector.save_news(news_items)
            
    except Exception as e:
        print(f"Ошибка при тестировании сбора новостей: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_news_collection() 