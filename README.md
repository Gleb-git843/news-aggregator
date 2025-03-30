# Агрегатор новостей

Веб-приложение для агрегации новостей из различных RSS-источников.

## Возможности

- Просмотр новостей с фильтрацией по категориям и источникам
- Управление источниками новостей (добавление, редактирование, удаление)
- Автоматический сбор новостей из RSS-фидов
- Адаптивный дизайн

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/news-aggregator.git
cd news-aggregator
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```
DATABASE_URL=sqlite:///./news.db
```

5. Инициализируйте базу данных:
```bash
python -m app.scripts.init_db
```

6. Добавьте начальные источники новостей:
```bash
python -m app.scripts.add_sources
```

## Запуск

1. Запустите приложение:
```bash
uvicorn main:app --reload
```

2. Откройте браузер и перейдите по адресу: http://localhost:8000

## API

API документация доступна по адресу: http://localhost:8000/docs

### Основные эндпоинты:

- GET /api/sources - получение списка источников
- POST /api/sources - создание нового источника
- GET /api/sources/{source_id} - получение информации об источнике
- PUT /api/sources/{source_id} - обновление информации об источнике
- DELETE /api/sources/{source_id} - удаление источника

## Структура проекта

```
news-aggregator/
├── app/
│   ├── api/
│   │   └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── news.py
│   ├── schemas/
│   │   └── news.py
│   ├── scripts/
│   │   ├── init_db.py
│   │   └── add_sources.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── index.html
│   │   └── sources.html
│   └── tasks/
│       └── news_collector.py
├── main.py
├── requirements.txt
└── README.md
```

## Лицензия

MIT 