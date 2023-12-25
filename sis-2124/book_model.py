from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для объявления моделей SQLAlchemy.
Base = declarative_base()

# Определение класса Book, представляющего сущность в базе данных.
class Book(Base):
    # Имя таблицы в базе данных.
    __tablename__ = 'books'
    # Определение столбцов таблицы и их типов данных.
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    genre = Column(String(50))

    # Метод для инициализации объекта Book через вызов экземпляра класса.
    def __call__(self, title, author, genre):
        # Создание нового экземпляра Book и инициализация его атрибутов.
        instance = Book()
        instance.title = title
        instance.author = author
        instance.genre = genre
        return instance
