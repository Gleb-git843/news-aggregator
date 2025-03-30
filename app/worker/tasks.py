from celery import Celery
from app.db.session import SessionLocal
from app.models.news import NewsSource
from app.services.news_collector import NewsCollector
from app.core.config import settings

celery_app = Celery(
    "news_collector",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1"
)

@celery_app.task
def collect_news():
    """Задача для сбора новостей из всех источников"""
    db = SessionLocal()
    try:
        collector = NewsCollector(db)
        sources = db.query(NewsSource).filter(NewsSource.is_active == True).all()
        
        for source in sources:
            try:
                if source.type == "RSS":
                    news_items = collector.collect_rss_feed(source)
                elif source.type == "WEBSITE":
                    news_items = collector.collect_website(source)
                else:
                    continue
                    
                collector.save_news(news_items)
            except Exception as e:
                print(f"Error collecting news from {source.url}: {str(e)}")
                continue
                
    finally:
        db.close() 