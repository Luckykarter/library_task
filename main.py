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
        new_book = cls(some_json.get('title'), some_json.get('author'), some_json.get('year'))
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
        self.library = [book.from_json() for book in self.library]
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

        for inx, book in enumerate(library.library):
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




parse = argparse.ArgumentParser("""Чтобы узнать нажмите:
                                    (l) - о наличии книг в библиотеке,
                                    (a) - добавить книгу,
                                    (s) - найти книгу по автору, по названию или по году выпуска,
                                    (d) - удалить книгу,
                                    (q) - для выхода из приложения
                                    """
                                )
parse.add_argument('-l', '--load', help='Показывает какие книги есть в библиотеке')
parse.add_argument('-a', '--add', help='Добавляет книгу в библиотеку')

# def hello():
#     print('Добро пожаловатьб чтобы вы хотели сделать?')
#
#
# def running_app():
#     print("Чтобы узнать нажмите:")
#     print("(1) - о наличии книг в библиотеке")
#     print("(2) - добавить книгу")
#     print("(3) - найти книгу по автору, по названию или по году выпуска")
#     print("(4) - удалить книгу")
#     print("q - для выхода из приложения")
#     my_lib = Library(FOLDER)
#     while True:
#         a = input('Введите что вы хотите сделать \n')
#         match a:
#             case '1':
#                 print(my_lib.load_books())
#             case '2':
#                 title = input("Введите название книги: \n")
#                 author = input("Введите автора книги \n")
#                 try:
#                     year = int(input("Введите год издания книги \n"))
#                 except ValueError as e:
#                     print('Вы указали не верный формат года')
#                 else:
#                     print(my_lib.add_book(title, author, year))
#             case '3':
#                 attribute_search = input('Введите атрибут для поиска книги \n')
#                 print(my_lib.search_book(attribute_search))
#             case '4':
#                 id_book = int(input('Введите id книги, которую вы хотите удалить'))
#                 print(my_lib.delete_book(id_book))
#             case 'q' | 'й':
#                 print('Всего хорошего')
#                 break
#             case _:
#                 print('Вы ввели не верное значение, попробуем все заново')
#                 running_app()
#
#
# def main():
hello()
running_app()

if __name__ == '__main__':
    main()
