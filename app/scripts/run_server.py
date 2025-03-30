import uvicorn
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_server():
    """
    Запускает сервер FastAPI
    """
    try:
        logger.info("Запуск сервера FastAPI...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Ошибка при запуске сервера: {str(e)}")

if __name__ == "__main__":
    run_server() 