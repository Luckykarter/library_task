import os
import json

FOLDER = 'C:/python_projects/llibrary_task/my_lib'


class Book:
    id = 0

    def __init__(self, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        self.id = self.get_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, author: {self.author}, year: {self.year}, status: {self.status}'

    @staticmethod
    def get_id():
        Book.id += 1
        return Book.id

    def json(self):
        result = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }
        return result

    def save(self, path: str):
        """
        Этот метод сохраняет в файл, что возвращает метот self.json()
        :param path: путь для создания файла и сохранения в нем
        :return: None
        """
        with open(os.path.join(path, f'{self.id}.json'), 'w') as file:
            json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        """
        Этот метод открывает файл с json-объектом и преобразовывает через метод from_json в объект класса Book
        :param filename: имя файла с json-объектом
        :return: экземпляр класса Book
        """
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
            return cls.from_json(content)

    @classmethod
    def from_json(cls, some_json) -> 'Book':
        """
        Этот метод создает новый объект класса Book используя JSON объек
        :param some_json: JSON объект
        :return: объъект класса Book
        """
        new_book = cls(some_json.get('title'), some_json.get('author'), some_json.get('year'))

        return new_book


class Library:
    def __init__(self, path: str, library: list = None) -> None:
        if library is None:
            library = []
        self.library = library
        self.path = path

    def add_book(self, title: str, author: str, year: int):
        book = Book(title, author, year)
        book.save(self.path)

    def delete_book(self, id: int):
        my_lib = self.load_books()
        for inx, book in enumerate(my_lib):
            if book.get(id) == id:
                del my_lib[inx]
                return f'{my_lib} \n Книга удалена успешно'
            else:
                return f'Книга с таким id: {id} не найденa'

    def load_books(self):
        """
        Метод проходит по полному пути заданный в data_path, проверяет каждый элемент в директории, если елемент формата
        json, то вызывает метод Book.load(). В итоге добавляет полученный объект класса Entry в entries
        :return: self.library
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        else:
            for item in os.listdir(self.path):
                if item.endswith('.json'):
                    item = Book.load(os.path.join(self.path, item))
                    self.library.append(item)
        return self.library

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
            if book.get(id) == id:
                book.status = status
                return book
            else:
                return 'Книга с таким статусом не найдена'


def main():
    mylib = Library(FOLDER)
    book1 = Book("Мертвые души", 'Гоголь', 2000)
    book2 = Book('Бессоница', "Стивен Кинг", 2006)
    book3 = Book('Евгений Онегин', 'Пушкин', 1999)

    book1.save(FOLDER)
    book2.save(FOLDER)
    book3.save(FOLDER)
    print(book1, book2, book3, sep='\n')

    print(mylib.load_books())


if __name__ == '__main__':
    main()
