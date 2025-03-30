import feedparser
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup
from app.models.news import News, Source
from app.core.config import settings
from sqlalchemy.orm import Session
import logging
from sqlalchemy import text
import requests
from requests.exceptions import Timeout

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self, db: Session):
        self.db = db
        self.timeout = 10  # Таймаут в секундах

    def collect_rss_feed(self, source: Source) -> List[News]:
        """
        Собирает новости из RSS-фида
        """
        try:
            # Используем requests для загрузки RSS с таймаутом
            response = requests.get(source.url, timeout=self.timeout)
            feed = feedparser.parse(response.content)
            
            news_items = []
            
            for entry in feed.entries:
                # Проверяем, существует ли уже такая новость
                existing_news = self.db.query(News).filter(
                    News.url == entry.link
                ).first()
                
                if existing_news:
                    continue
                
                # Извлекаем описание
                description = None
                if hasattr(entry, 'description'):
                    description = entry.description
                elif hasattr(entry, 'summary'):
                    description = entry.summary
                
                # Извлекаем дату публикации
                published_at = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    published_at = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    published_at = datetime(*entry.updated_parsed[:6])
                
                # Определяем категорию
                category = self.detect_category(entry.title, description)
                
                news = News(
                    title=entry.title,
                    description=description,
                    url=entry.link,
                    published_at=published_at,
                    category=category,
                    source_id=source.id
                )
                
                news_items.append(news)
            
            return news_items
            
        except Timeout:
            print(f"Таймаут при сборе новостей из {source.url}")
            return []
        except Exception as e:
            print(f"Ошибка при сборе новостей из {source.url}: {str(e)}")
            return []

    def detect_category(self, title: str, description: Optional[str] = None) -> str:
        """
        Определяет категорию новости на основе заголовка и описания
        """
        text = f"{title} {description or ''}".lower()
        
        categories = {
            "политика": ["политика", "государство", "правительство", "президент", "министр", "выборы"],
            "экономика": ["экономика", "финансы", "рынок", "банк", "инвестиции", "курс", "доллар", "евро"],
            "технологии": ["технологии", "интернет", "гаджеты", "смартфон", "компьютер", "искусственный интеллект"],
            "спорт": ["спорт", "футбол", "хоккей", "чемпионат", "матч", "игра"],
            "общество": ["общество", "культура", "образование", "здравоохранение", "социальные"],
            "наука": ["наука", "исследование", "ученые", "открытие", "эксперимент"],
            "развлечения": ["развлечения", "кино", "музыка", "телевидение", "шоу", "звезды"],
            "происшествия": ["происшествие", "авария", "пожар", "преступление", "инцидент"],
            "международные": ["международные", "зарубежные", "мировые", "глобальные"],
            "региональные": ["регион", "город", "область", "край", "район"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return "общее"

    def save_news(self, news_items: List[Dict]):
        """Сохранение новостей в базу данных"""
        for item in news_items:
            # Проверка на дубликаты
            existing_news = self.db.query(News).filter(News.url == item["url"]).first()
            if not existing_news:
                news = News(**item)
                self.db.add(news)
        
        self.db.commit() 