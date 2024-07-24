# install python<=3.10

import argparse
import json

FOLDER = 'lib.json'


class Book:

    def __init__(self, id: int, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, author: {self.author}, year: {self.year}, status: {self.status}'

    def json(self):
        result = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }
        return result

    @classmethod
    def from_json(cls, some_json):
        new_book = cls(some_json.get('id'), some_json.get('title'), some_json.get('author'), int(some_json.get('year')))
        return new_book


class Library:
    def __init__(self, path: str, library: list = None) -> None:
        if library is None:
            library = []
        self.library = library
        self.path = path

    def __enter__(self):
        self.library = self.load_library()  # загрузить из файла на входе
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_library()  # сохранить в файл на выходе

    def load_library(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.library = json.loads(f.read())
        self.library = [Book.from_json(book) for book in self.library]
        return self.library

    def save_library(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps([book.json() for book in self.library]))

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Добавляет книгу в список self.library
        :param title: Название книги
        :param author: Автор
        :param year: Год выпуска
        :return: str
        """
        id_book = len(self.library) + 1
        book = Book(id_book, title, author, year)
        self.library.append(book)

    def delete_book(self, id: int) -> str:
        """
        Метод удаляет из файла книгу по его id
        :param id: id книги
        :return: Сообщение об удалении / Сообщение об ошибки при удалении
        """

        for inx, book in enumerate(self.library):
            if book.id == id:
                del self.library[inx]
                return f'{self.library} \n Книга удалена успешно'

        return f'Книга с таким id: {id} не найденa'

    def load_books(self) -> list:
        """
        Этот метод пытается найти файл self.path и прочитать его. Если файл существует, он читает и
        преобразовывает текст файла в объект List
        :return: list(Books)
        """

        return self.library

    def search_book(self, some_item) -> dict:
        """
        Этот метод ищет книгу по заданному параметру и возвращает эту книгу
        :param some_item: любой возможный аргумент для поиска(по имени, по автору, по году)
        :return: dict
        """
        for inx, book in enumerate(self.library):
            if isinstance(int(some_item), int):
                if some_item == book.year:
                    return book
            else:
                if some_item == book.title:
                    return book
                if some_item == book.author:
                    return book
        return 'Такой книги не существует'


    def change_status(self, id: int, status: str) -> Book:
        """
        Этот метод меняет статус книги на новый и записывает в файл новые данные
        :param id: Айди книги
        :param status: новый статус для книги
        :return: Book
        """

        for book in self.library:
            if id == book.id:
                book.status = status
                return book

        return f'Книга с таким id: {id} не найденa'


def main():
    with Library(FOLDER) as library:

        parser = argparse.ArgumentParser(description="""Manage library with load, add, delete, search, and change commands""")

        subparsers = parser.add_subparsers(title="Commands", description="""Загрузка всех книг-load, добавить книгу-add,
                                                                            удалить книгу-delete, для поиска книги-search,
                                                                            изменить статус-change""",
                                           help="Use one of these commands")
        # Load command
        parser_load = subparsers.add_parser('load', help='Загружает все книги из библиотеки')
        parser_load.set_defaults(func=library.load_books)

        # Add command
        parser_add = subparsers.add_parser('add', help='Добавляет новую книгу в библиотеку')
        parser_add.add_argument('title', type=str, help='Название книги')
        parser_add.add_argument('author', type=str, help='Имя автора')
        parser_add.add_argument('year', type=int, help='Год выпуска')
        parser_add.set_defaults(func=library.add_book)

        # Delete command
        parser_delete = subparsers.add_parser('delete', help='Удаляет книгу по заданому id')
        parser_delete.add_argument('id', type=int, help='ID книги, которую удалить')
        parser_delete.set_defaults(func=library.delete_book)


        #Search command
        parser_search = subparsers.add_parser('search', help='Ищет книгу по заданному аргументу')
        parser_search.add_argument('item', type=str, help='Поиск книги по заданой информации')
        parser_search.set_defaults(func=library.search_book)

        # Change command
        parser_change = subparsers.add_parser('change', help='Заменяет статус книги')
        parser_change.add_argument('id', type=int, help='ID книги из которой нужно изменить статус')
        parser_change.add_argument('status', type=str, help='The item to change')
        parser_change.set_defaults(func=library.change_status)

        args = parser.parse_args()

        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()







if __name__ == '__main__':
    main()
