import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name=__name__, log_file='bot.log', level=logging.INFO, max_bytes=5_000_000, backup_count=3):
    """
    Настройка логгера: вывод в консоль и в файл с ротацией.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Хендлер для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Хендлер для файла с ротацией
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Создаём глобальный логгер для всего приложения
log = setup_logger('VKBot', 'vk_bot.log')