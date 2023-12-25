from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для объявления моделей SQLAlchemy.
Base = declarative_base()

# Определение класса Person, представляющего сущность в базе данных.
class Person(Base):
    # Имя таблицы в базе данных.
    __tablename__ = 'persons'

    # Определение столбцов таблицы и их типов данных.
    id = Column(Integer, primary_key=True)
    _name = Column(String)
    _uni = Column(String)

    # Конструктор класса, инициализирующий объект Person.
    def __init__(self, name, uni):
        self.name = name
        self.uni = uni

    # Свойство name с геттером и сеттером.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Проверка на пустую строку или неверный тип данных.
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    # Свойство uni с геттером и сеттером.
    @property
    def uni(self):
        return self._uni

    @uni.setter
    def uni(self, value):
        # Проверка на пустую строку или неверный тип данных.
        if not value or not isinstance(value, str):
            raise ValueError("University must be a non-empty string.")
        self._uni = value

    # Метод для инициализации объекта через вызов экземпляра класса.
    def __call__(self, name, uni):
        self.name = name
        self.uni = uni
        return self
