import asyncio
import aiohttp
import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.news import Source, News
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_feed(session: aiohttp.ClientSession, source: Source) -> list:
    """
    Получение новостей из RSS-фида
    """
    try:
        async with session.get(source.url) as response:
            if response.status == 200:
                content = await response.text()
                feed = feedparser.parse(content)
                return feed.entries
            else:
                logger.error(f"Ошибка при получении фида {source.name}: {response.status}")
                return []
    except Exception as e:
        logger.error(f"Ошибка при обработке фида {source.name}: {str(e)}")
        return []

async def process_entries(db: Session, source: Source, entries: list):
    """
    Обработка записей из фида
    """
    for entry in entries:
        try:
            # Проверяем, существует ли уже такая новость
            existing_news = db.query(News).filter(News.url == entry.link).first()
            if existing_news:
                continue

            # Получаем описание новости
            description = ""
            if hasattr(entry, 'description'):
                description = entry.description
            elif hasattr(entry, 'summary'):
                description = entry.summary
            elif hasattr(entry, 'content'):
                if isinstance(entry.content, list):
                    description = entry.content[0].value
                else:
                    description = entry.content

            # Получаем дату публикации
            published_at = datetime.utcnow()
            if hasattr(entry, 'published_parsed'):
                published_at = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed'):
                published_at = datetime(*entry.updated_parsed[:6])

            # Получаем категорию
            category = "other"
            if hasattr(entry, 'tags') and entry.tags:
                if isinstance(entry.tags, list):
                    category = entry.tags[0].get('term', 'other')
                else:
                    category = entry.tags.get('term', 'other')

            # Создаем новую новость
            news = News(
                title=entry.title,
                description=description,
                url=entry.link,
                published_at=published_at,
                category=category,
                source_id=source.id
            )
            db.add(news)
        except Exception as e:
            logger.error(f"Ошибка при обработке записи {entry.get('title', 'Unknown')}: {str(e)}")
            continue

async def collect_news():
    """
    Сбор новостей из всех активных источников
    """
    db = SessionLocal()
    try:
        # Получаем все активные источники
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        async with aiohttp.ClientSession() as session:
            for source in sources:
                logger.info(f"Обработка источника: {source.name}")
                entries = await fetch_feed(session, source)
                await process_entries(db, source, entries)
        
        db.commit()
        logger.info("Сбор новостей завершен успешно")
        
    except Exception as e:
        logger.error(f"Ошибка при сборе новостей: {str(e)}")
        db.rollback()
    finally:
        db.close()

async def collect_news_task():
    """
    Фоновая задача для сбора новостей
    """
    while True:
        await collect_news()
        await asyncio.sleep(settings.NEWS_COLLECTION_INTERVAL) 