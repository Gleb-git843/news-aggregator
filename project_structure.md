# Структура проекта MyWinNewsAPP

## Диаграмма структуры проекта

```mermaid
graph TD
    A[MyWinNewsAPP] --> B[app/]
    A --> C[scripts/]
    A --> D[requirements.txt]
    A --> E[.env]
    A --> F[main.py]
    
    B --> G[api/]
    B --> H[core/]
    B --> I[models/]
    B --> J[schemas/]
    B --> K[services/]
    B --> L[templates/]
    B --> M[static/]
    B --> N[tasks/]
    B --> O[worker/]
    
    G --> P[endpoints/]
    H --> Q[database.py]
    H --> R[config.py]
    I --> S[news.py]
    J --> T[news.py]
    K --> U[news_collector.py]
    
    C --> V[init_db.py]
    C --> W[add_sources.py]
    C --> X[create_db.py]
```

## Диаграмма зависимостей

```mermaid
graph LR
    A[FastAPI] --> B[SQLAlchemy]
    A --> C[Pydantic]
    A --> D[Jinja2]
    A --> E[Uvicorn]
    
    B --> F[PostgreSQL]
    
    G[NewsCollector] --> H[Feedparser]
    G --> I[BeautifulSoup4]
    G --> B
    
    J[Celery] --> K[Redis]
    
    L[Web Interface] --> A
    L --> D
```

## Основные компоненты

1. **API Layer**
   - FastAPI endpoints для REST API
   - Pydantic модели для валидации данных

2. **Data Layer**
   - SQLAlchemy модели
   - PostgreSQL база данных

3. **Service Layer**
   - NewsCollector для сбора новостей
   - Feedparser для парсинга RSS
   - BeautifulSoup4 для парсинга веб-страниц

4. **Task Processing**
   - Celery для асинхронных задач
   - Redis как брокер сообщений

5. **Web Interface**
   - Jinja2 шаблоны
   - Статические файлы

6. **Configuration**
   - .env файл для переменных окружения
   - config.py для настроек приложения

7. **Database Management**
   - Скрипты инициализации и миграции
   - Управление источниками новостей 