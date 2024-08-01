# install python<=3.10
import os.path
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict

from literals import BOOK_DOES_NOT_EXIST, NO_BOOKS_IN_LIBRARY, BOOK_NOT_FOUND

FOLDER = 'lib.json'


def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=lambda x: len(str(x)))))

    separator = "-+-".join('-' * n for n in col_width)

    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            print(separator)

        result = []
        for col in range(cols):
            item = str(data[row][col]).rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: str = 'в наличии'

    def __str__(self):
        for k, v in asdict(self).items():
            print(f'{k}\t{v}')


class Library:
    def __init__(self, path: str) -> None:
        self.library: Dict[int: Book] = {}
        self.path = path

    def __enter__(self):
        self.library = self.load_library()  # загрузить из файла на входе
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_library()  # сохранить в файл на выходе

    def load_library(self) -> dict:
        if not os.path.isfile(self.path):
            return {}
        with open(self.path, 'r', encoding='utf-8') as f:
            library = json.loads(f.read())
            for k, v in library.items():
                library[k] = Book(**v)
        return library

    def save_library(self):
        if self.library:
            with open(self.path, 'w', encoding='utf-8') as f:
                lib_json = {k: asdict(v) for k, v in self.library.items()}
                f.write(json.dumps(lib_json))

    def add_book(self, **kwargs) -> Book:
        book_id = len(self.library) + 1
        book = Book(id=book_id, **kwargs)
        self.library[book_id] = book
        return book

    def delete_book(self, book_id: int):
        if book_id not in self.library:
            raise KeyError(BOOK_DOES_NOT_EXIST.format(book_id=book_id))
        return self.library.pop(book_id)

    def show_books(self):
        if not self.library:
            print(NO_BOOKS_IN_LIBRARY)
            return
        table_library = [list(asdict(next(iter(self.library.values()))).keys())]
        for book in self.library.values():
            table_library.append(list(asdict(book).values()))
        print_pretty_table(table_library)

    def search_book(self, search_string: str) -> Book:
        for book in self.library.values():
            if any((search_string == book.title,
                    search_string == book.author,
                    search_string == str(book.year))):
                return book
        raise KeyError(BOOK_NOT_FOUND.format(search_string))

    def change_status(self, book_id: int, status: str) -> Book:
        if book_id not in self.library:
            raise KeyError(BOOK_DOES_NOT_EXIST.format(book_id=book_id))
        self.library[book_id].status = status
        return self.library[book_id]


def add_book(library: Library, args):
    kwargs = vars(args)
    kwargs.pop('func')
    book = library.add_book(**kwargs)
    print(f"Book {book} successfully added")


def show_books(library: Library, arg):
    library.show_books()


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
    parser_load.set_defaults(func=show_books)

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
            args.func(library, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
