from library_bot import LibraryBot
from library_api import LibraryApi

# Токен вашего бота Telegram.
bot_token = '6465863820:AAE1wXJ4PxlxP6AwPxDhZ6-LPdjDvSjWY14'
# Строка подключения к базе данных (в данном случае, SQLite).
db_connection_string = 'sqlite:///example.db'
# Создание экземпляра LibraryApi.
library_api = LibraryApi()

if __name__ == "__main__":
    # Создание экземпляра LibraryBot с передачей токена и строки подключения к базе данных.
    library_bot = LibraryBot(bot_token, db_connection_string)
    # Запуск бота.
    library_bot.run()
