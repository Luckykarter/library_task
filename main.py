# install python<=3.10
import os.path
import argparse
import json

FOLDER = 'lib.json'


def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    separator = "-+-".join('-' * n for n in col_width)

    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            print(separator)

        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))


class Book:

    def __init__(self, id: int, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f'{self.id}, {self.title}, {self.author}, {self.year}, {self.status}'

    def value(self):
        return self.id, self.title, self.author, self.year, self.status

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

    def load_library(self)-> list:
        """
        Метод ппроверяет, есть ли в ппути файл, если его нет то возвращает пусстой список. В другом случае открывает
        файл преобразовывает значения файлов в экземпляры класса Book, записывает в список self.library
        :return: self.library
        """
        if not os.path.isfile(self.path):
            return []
        with open(self.path, 'r', encoding='utf-8') as f:
            self.library = json.loads(f.read())
        self.library = [Book.from_json(book) for book in self.library]
        return self.library

    def save_library(self):
        if self.library:
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
        if len(self.library) > 0:
            id_book = self.library[len(self.library) - 1].id + 1
        else:
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
                self.load_books()
                return 'Книга удалена успешно'

        return f'Книга с таким id: {id} не найденa'

    def load_books(self) -> str:
        """
        Этот метод проходит по списку книг(self.library), преобразуя каждую книгу в список атрибутов, передает
        в функцию print_pretty_table. Эта функция выводит в табличном стиле
        :return: str
        """

        table_library = [['ID', 'TITLE', 'AUTHOR', 'YEAR', 'STATUS']]
        for book in self.library:
            table_library.append([str(value) for value in book.value()])

        print_pretty_table(table_library)

    def search_book(self, some_item) -> dict:
        """
        Этот метод ищет книгу по заданному параметру и возвращает эту книгу
        :param some_item: любой возможный аргумент для поиска(по имени, по автору, по году)
        :return: dict
        """
        try:
            some_item = int(some_item)
        except ValueError:
            pass
        else:
            for inx, book in enumerate(self.library):
                if some_item == book.year:
                    return str(book)

        for inx, book in enumerate(self.library):
            if some_item == book.title:
                return str(book)
            if some_item == book.author:
                return str(book)
        return 'Такой книги нет в наличии'

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
                return self.load_books()


        return f'Книга с таким id: {id} не найденa'


def add_book(library: Library, args):
    library.add_book(args.title, args.author, args.year)


def load_books(library: Library, arg):
    return library.load_books()


def delete_book(library: Library, args):
    return library.delete_book(args.id)


def change_status(library: Library, args):
    return library.change_status(args.id, args.status)


def search_book(library: Library, arg):
    return library.search_book(arg.item)


def main():
    parser = argparse.ArgumentParser(
        description="""Manage library with load, add, delete, search, and change commands""")

    subparsers = parser.add_subparsers(title="Commands", description="""Загрузка всех книг-load, добавить книгу-add,
                                                                        удалить книгу-delete, для поиска книги-search,
                                                                        изменить статус-change""",
                                       help="Use one of these commands")
    # Add command
    parser_add = subparsers.add_parser('add',
                                       help='Добавляет новую книгу в библиотеку: название, автор, год выпуска')
    parser_add.add_argument('title', type=str, help='Название книги')
    parser_add.add_argument('author', type=str, help='Имя автора')
    parser_add.add_argument('year', type=int, help='Год выпуска')
    parser_add.set_defaults(func=add_book)

    # Delete command
    parser_delete = subparsers.add_parser('delete', help='Удаляет книгу по заданому id')
    parser_delete.add_argument('id', type=int, help='ID книги, которую удалить')
    parser_delete.set_defaults(func=delete_book)

    # Load
    parser_load = subparsers.add_parser('load', help='Выводит все книги из файла')
    parser_load.set_defaults(func=load_books)

    # Search command
    parser_search = subparsers.add_parser('search', help='Ищет книгу по заданному аргументу(название, автор, год)')
    parser_search.add_argument('item', type=str, help='Поиск книги по заданой информации')
    parser_search.set_defaults(func=search_book)

    # Change command
    parser_change = subparsers.add_parser('change', help='Заменяет статус книги, принимает id-книги, новый статус')
    parser_change.add_argument('id', type=int, help='ID книги из которой нужно изменить статус')
    parser_change.add_argument('status', type=str, help='The item to change')
    parser_change.set_defaults(func=change_status)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        with Library(FOLDER) as library:
            print(args.func(library, args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
