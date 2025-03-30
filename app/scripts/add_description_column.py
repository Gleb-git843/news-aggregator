import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import psycopg2
from app.core.config import settings

def add_description_column():
    """
    Добавляет столбец description в таблицу news
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
        
        # Выполняем SQL-команду
        cur.execute("ALTER TABLE news ADD COLUMN IF NOT EXISTS description TEXT;")
        
        # Подтверждаем изменения
        conn.commit()
        print("Столбец description успешно добавлен!")
        
    except Exception as e:
        print(f"Ошибка при добавлении столбца: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Добавление столбца description...")
    add_description_column() 