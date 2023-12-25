import telebot

# Класс для регистрации команд бота.
class BotCommands:
    # Конструктор класса, принимающий токен бота и объект LibraryApi.
    def __init__(self, bot_token, library_api):
        # Создание объекта TeleBot с использованием переданного токена бота.
        self.bot = telebot.TeleBot(bot_token)
        # Объект LibraryApi для выполнения операций с библиотекой.
        self.library_api = library_api

        # Регистрация команд.
        self.register_commands()

    # Метод для регистрации команд бота.
    def register_commands(self):
        # Обработчик команды /get_books.
        @self.bot.message_handler(commands=['get_books'])
        def handle_get_books(message):
            try:
                # Извлечение поискового запроса из текста сообщения.
                search_query = message.text.split(' ', 1)[1]
                # Получение списка книг с использованием LibraryApi.
                books = self.library_api.get_books(search_query)

                if books:
                    books_info = "Books Found:\n"
                    for book in books:
                        books_info += f"{book.title} by {book.author}\n"
                else:
                    books_info = "No books found."

                # Отправка сообщения с информацией о найденных книгах.
                self.bot.send_message(message.chat.id, books_info)
            except RuntimeError as e:
                # Обработка ошибок и отправка сообщения о возникшей проблеме.
                self.bot.send_message(message.chat.id, f"Error getting books from the API. {e}")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Unexpected error: {e}")
