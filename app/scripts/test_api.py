import requests
import json
from datetime import datetime, timedelta

def test_api():
    """
    Тестирует основные эндпоинты API
    """
    base_url = "http://localhost:8000/api/v1"
    
    print("\nТестирование API новостей")
    print("-------------------------")
    
    # Тест получения списка новостей
    print("\n1. Получение списка новостей:")
    response = requests.get(f"{base_url}/news/")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество новостей: {len(data)}")
        if len(data) > 0:
            print("\nПример первой новости:")
            print(json.dumps(data[0], ensure_ascii=False, indent=2))
    
    # Тест получения новостей по категории
    print("\n2. Получение новостей по категории 'Политика':")
    response = requests.get(f"{base_url}/news/?category=Политика")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество новостей: {len(data)}")
    
    # Тест получения новостей по источнику
    print("\n3. Получение новостей из ТАСС:")
    response = requests.get(f"{base_url}/news/?source=ТАСС")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество новостей: {len(data)}")
    
    # Тест получения новостей за последние 24 часа
    print("\n4. Получение новостей за последние 24 часа:")
    response = requests.get(f"{base_url}/news/?hours=24")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество новостей: {len(data)}")
    
    # Тест получения статистики
    print("\n5. Получение статистики:")
    response = requests.get(f"{base_url}/news/stats/")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_api() 