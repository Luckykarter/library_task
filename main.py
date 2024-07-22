import os
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



class Library:
    def __init__(self, path: str, library: list = None) -> None:
        if library is None:
            library = []
        self.library = library
        self.path = path

    def add_book(self, title: str, author: str, year: int):
        id_book = len(self.library) + 1
        book = Book(id_book, title, author, year)
        self.library.append(book.json())
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.library, ensure_ascii=False))

    def delete_book(self, id: int):
        my_lib = self.load_books()
        for inx, book in enumerate(my_lib):
            if book.get('id') == id:
                del my_lib[inx]
                with open(self.path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(my_lib, ensure_ascii=False))
                return f'{my_lib} \n Книга удалена успешно'

        return f'Книга с таким id: {id} не найденa'

    def load_books(self):
        """
        Метод проходит по полному пути заданный в data_path, проверяет каждый элемент в директории, если елемент формата
        json, то вызывает метод Book.load(). В итоге добавляет полученный объект класса Entry в entries
        :return: self.library
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                my_lib = file.read()
        except FileNotFoundError:
            return f'Такого файла не существует'
        else:
            return json.loads(my_lib)

    def search_book(self, some_item):
        my_lib = self.load_books()
        for inx, book in enumerate(my_lib):
            if isinstance(some_item, int):
                if some_item == book.get('year'):
                    return book
            else:
                if some_item == book.get('title'):
                    return book
                if some_item == book.get('author'):
                    return book

    def change_status(self, id: int, status: str):
        my_lib = self.load_books()
        for book in my_lib:
            if id == book.get('id'):
                book['status'] = status
                with open(self.path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(my_lib, ensure_ascii=False))
                return book

        return f'Книга с таким id: {id} не найденa'


def main():
    my_library = Library(FOLDER)
    print(my_library.load_books())
    print(my_library.delete_book(2))
    print(my_library.load_books())


if __name__ == '__main__':
    main()
