import requests


# Класс для взаимодействия с внешним API (Open Library API).
class LibraryApi:
    # Конструктор класса, принимающий базовый URL для API (по умолчанию, Open Library API).
    def __init__(self, api_base_url='https://openlibrary.org/api/'):
        self.api_base_url = api_base_url

    # Внутренний класс Book для представления информации о книге.
    class Book:
        # Конструктор класса Book, инициализирующий объект книги с указанием заголовка и автора.
        def __init__(self, title, author):
            self.title = title
            self.author = author

    # Метод для получения списка книг по заданному поисковому запросу и типу поиска.
    def get_books(self, search_query, search_type='q', page=1):
        try:
            # Параметры для запроса к API (поисковый запрос, тип поиска, номер страницы).
            params = {
                search_type: search_query,
                'page': page
            }

            # Отправка GET-запроса к API с использованием библиотеки requests.
            response = requests.get(f"{self.api_base_url}search.json", params=params)
            response.raise_for_status()

            # Обработка ответа от API в формате JSON.
            data = response.json()

            # Если в ответе есть 'docs', извлечение информации о книгах.
            if 'docs' in data:
                books = []
                for book_data in data['docs']:
                    title = book_data.get('title', 'N/A')
                    author = book_data.get('author_name', ['N/A'])[0]
                    # Создание объекта Book для каждой найденной книги.
                    book = self.Book(title=title, author=author)
                    books.append(book)
                return books
            else:
                return []
        except requests.exceptions.RequestException as e:
            # В случае ошибки при подключении к API, генерация исключения с сообщением.
            raise RuntimeError(f"Error connecting to the API: {e}")
