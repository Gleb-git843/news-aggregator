# News Aggregator

Приложение для агрегации новостей из различных источников с возможностью фильтрации по категориям, источникам и времени.

## Возможности

- Сбор новостей из различных источников
- Фильтрация новостей по:
  - Категориям
  - Источникам
  - Времени публикации
- REST API для работы с новостями
- Статистика по новостям

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Gleb-git843/news-aggregator.git
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

4. Создайте файл .env на основе .env.example и настройте параметры подключения к базе данных

5. Создайте базу данных и таблицы:
```bash
python -m app.scripts.create_db
```

6. Запустите сервер:
```bash
python -m app.scripts.run_server
```

## API Endpoints

- `GET /api/v1/news/` - получение списка новостей
- `GET /api/v1/news/stats` - получение статистики
- `GET /api/v1/news/categories` - получение списка категорий
- `GET /api/v1/news/sources/` - получение списка источников

## Параметры фильтрации

- `category` - фильтр по категории
- `source` - фильтр по источнику
- `hours` - фильтр по времени (последние N часов)

## Лицензия

MIT
