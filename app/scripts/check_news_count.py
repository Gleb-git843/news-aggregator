import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import psycopg2
from app.core.config import settings

def check_news_count():
    """
    Проверяет количество новостей в базе данных
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
        
        # Получаем общее количество новостей
        cur.execute("SELECT COUNT(*) FROM news;")
        total_count = cur.fetchone()[0]
        print(f"\nВсего новостей в базе: {total_count}")
        
        # Получаем количество новостей по источникам
        cur.execute("""
            SELECT s.name, COUNT(n.id) as count
            FROM sources s
            LEFT JOIN news n ON s.id = n.source_id
            GROUP BY s.name;
        """)
        
        print("\nКоличество новостей по источникам:")
        print("-----------------------------------")
        for source_name, count in cur.fetchall():
            print(f"{source_name}: {count}")
        
    except Exception as e:
        print(f"Ошибка при проверке количества новостей: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_news_count() 