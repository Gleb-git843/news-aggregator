import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import psycopg2
from app.core.config import settings

def show_table_structure():
    """
    Показывает структуру таблицы news
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
        
        # Выполняем SQL-запрос для получения информации о столбцах
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'news'
            ORDER BY ordinal_position;
        """)
        
        # Получаем и выводим результаты
        columns = cur.fetchall()
        print("\nСтруктура таблицы news:")
        print("------------------------")
        for column in columns:
            print(f"Столбец: {column[0]}")
            print(f"Тип: {column[1]}")
            print(f"Может быть NULL: {column[2]}")
            print("------------------------")
        
    except Exception as e:
        print(f"Ошибка при получении структуры таблицы: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    show_table_structure() 