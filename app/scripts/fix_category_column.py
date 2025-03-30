import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import psycopg2
from app.core.config import settings

def fix_category_column():
    """
    Создает тип newscategory и изменяет тип столбца category
    """
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=5432  # Стандартный порт PostgreSQL
        )
        
        # Создаем курсор
        cur = conn.cursor()
        
        # Читаем SQL-файл с указанием кодировки
        with open(os.path.join(os.path.dirname(__file__), 'fix_category_column.sql'), 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Выполняем SQL-команды
        cur.execute(sql)
        
        # Подтверждаем изменения
        conn.commit()
        print("Тип newscategory успешно создан и применен к столбцу category!")
        
    except Exception as e:
        print(f"Ошибка при изменении типа столбца: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Исправление типа столбца category...")
    fix_category_column() 