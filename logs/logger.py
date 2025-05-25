import logging
from datetime import datetime

# Настройка логгера
logger = logging.getLogger("mathbot")
logger.setLevel(logging.DEBUG)

# Создаём обработчик
file_handler = logging.FileHandler(f"logs/mathbot_{datetime.now().date()}.log", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(file_handler)

# Пример использования
if __name__ == "__main__":
    logger.info("Пример: бот запущен")
    logger.warning("Пример: предупреждение")
    logger.error("Пример: ошибка")
