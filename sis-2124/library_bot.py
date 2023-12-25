import telebot
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from person import Person
from library_api import LibraryApi
from book_model import Book
from bot_logger import BotLogger
import requests

# Класс LibraryBot представляет собой телеграм-бот для взаимодействия с виртуальной библиотекой.
class LibraryBot:
    def __init__(self, bot_token, db_connection_string):
        self.logger = BotLogger()
        self.Book = Book()
        self.library_api = LibraryApi()
        self.bot = telebot.TeleBot(bot_token)
        self.engine = create_engine(db_connection_string, echo=True)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Person = Person

        # Инициализация базы данных.
        self.init_db()
        # Регистрация обработчиков сообщений.
        self.register_handlers()

    # Инициализация базы данных, создание таблиц Book и Person.
    def init_db(self):
        try:
            Book.metadata.create_all(bind=self.engine)
            Person.metadata.create_all(bind=self.engine)
        except Exception as e:
            self.logger.log_exception(f"Error initializing the database: {e}")

    # Регистрация обработчиков команд бота.
    def register_handlers(self):
        # Обработчик команды /start.
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.bot.send_message(message.chat.id, "Welcome! I am your library bot. By Adilet, Zhibek, Aruzhan. Type /help for assistance.")

        # Обработчик команды /help.
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.bot.send_message(message.chat.id,
                                  "This bot allows you to interact with a virtual library. You can add books, "
                                  "view the library, search books, and etc. Our goal was to create a bot to help search for different books.")

        # Обработчик команды /add_book.
        @self.bot.message_handler(commands=['add_book'])
        def handle_add_book(message):
            try:
                # Получение информации о книге из текста сообщения.
                book_info = message.text.split(' ', 1)[1]
                title, author, genre = map(str, book_info.split(','))

                # Создание новой книги и добавление в базу данных.
                new_book = self.Book(title=title, author=author, genre=genre)
                self.session.add(new_book)
                self.session.commit()

                self.bot.send_message(message.chat.id, f"Book '{title}' added successfully!")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error adding the book. {e}")

        # Обработчик команды /add_person.
        @self.bot.message_handler(commands=['add_person'])
        def handle_add_person(message):
            try:
                # Получение информации о человеке из текста сообщения.
                person_info = message.text.split(' ', 1)[1]
                name, uni = map(str, person_info.split(','))

                # Создание нового человека и добавление в базу данных.
                new_person = Person(name=name, uni=uni)
                self.session.add(new_person)
                self.session.commit()

                self.bot.send_message(message.chat.id, f"Person '{name}' added successfully!")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error adding the person. {e}")

        # Обработчик команды /view_library.
        @self.bot.message_handler(commands=['view_library'])
        def handle_view_library(message):
            try:
                # Получение списка книг из базы данных.
                books = self.session.query(Book).all()

                if books:
                    library_text = "Library Contents:\n"
                    for book in books:
                        library_text += f"{book.title} by {book.author} - {book.genre}\n"
                else:
                    library_text = "The library is empty."

                self.bot.send_message(message.chat.id, library_text)

                self.session.commit()
                self.session.close()
            except Exception as e:
                self.logger.log_exception(f"Error handling view library: {e}")
                self.bot.send_message(message.chat.id, "An error occurred while handling the request.")

        # Обработчик команды /delete_book.
        @self.bot.message_handler(commands=['delete_book'])
        def handle_delete_book(message):
            try:
                # Получение названия книги из текста сообщения.
                book_title = message.text.split(' ', 1)[1]
                # Поиск книги в базе данных.
                book = self.session.query(self.Book).filter_by(title=book_title).first()

                if book:
                    # Удаление книги из базы данных.
                    self.session.delete(book)
                    self.session.commit()
                    self.bot.send_message(message.chat.id, f"Book '{book_title}' deleted successfully!")
                else:
                    self.bot.send_message(message.chat.id, f"Book '{book_title}' not found.")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error deleting the book. {e}")

        # Обработчик команды /search_book.
        @self.bot.message_handler(commands=['search_book'])
        def handle_search_book(message):
            try:
                # Извлечение названия книги из команды.
                book_title = message.text.split(' ', 1)[1]

                # Поиск книг с использованием Open Library API.
                api_url = 'https://openlibrary.org/search.json'
                params = {'q': book_title}
                response = requests.get(api_url, params=params)
                response.raise_for_status()

                data = response.json()

                if 'docs' in data:
                    books_info = "Books Found:\n"
                    for book_data in data['docs']:
                        title = book_data.get('title', 'N/A')
                        author = book_data.get('author_name', ['N/A'])[0]
                        books_info += f"{title} by {author}\n"
                    self.bot.send_message(message.chat.id, books_info)
                else:
                    self.bot.send_message(message.chat.id, f"No books found with the title '{book_title}'.")
            except requests.exceptions.RequestException as e:
                self.logger.log_exception(f"Error searching for the book using the API: {e}")
                self.bot.send_message(message.chat.id, "An error occurred while searching for the book.")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Unexpected error: {e}")


    def run(self):
        self.bot.polling(none_stop=True)

    def Book(self, title, author, genre):
        pass