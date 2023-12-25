import logging

# Класс для логгирования исключений бота в файл.
class BotLogger:
    # Конструктор класса, принимающий имя файла для логов (по умолчанию 'bot_log.txt').
    def __init__(self, log_file='bot_log.txt'):
        # Настройка логгера с указанием файла для логов, уровня логирования (ERROR), и формата записей.
        logging.basicConfig(filename=log_file, level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    # Метод для логгирования исключения.
    def log_exception(self, exception_message):
        # Запись исключения в лог с использованием метода logging.exception().
        logging.exception(exception_message)
