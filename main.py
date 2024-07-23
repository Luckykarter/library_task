#install python<=3.10


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

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Записывает книгу в файл по пути self.path
        :param title: Название книги
        :param author: Автор
        :param year: Год выпуска
        :return: str
        """
        id_book = len(self.library) + 1
        book = Book(id_book, title, author, year)
        self.library.append(book.json())
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.library, ensure_ascii=False))
        return f'Книга {book} успешно добавлена'

    def delete_book(self, id: int) -> str:
        """
        Метод удаляет из файла книгу по его id
        :param id: id книги
        :return: Сообщение об удалении / Сообщение об ошибки при удалении
        """
        my_lib = self.load_books()
        for inx, book in enumerate(my_lib):
            if book.get('id') == id:
                del my_lib[inx]
                with open(self.path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(my_lib, ensure_ascii=False))
                return f'{my_lib} \n Книга удалена успешно'

        return f'Книга с таким id: {id} не найденa'

    def load_books(self) -> list:
        """
        Этот метод пытается найти файл self.path и прочитать его. Если файл существует, он читает и
        преобразовывает текст файла в объект List
        :return: list(dict) or str
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                my_lib = file.read()
        except FileNotFoundError:
            return f'Такого файла не существует'
        else:
            return json.loads(my_lib)

    def search_book(self, some_item) -> dict:
        """
        Этот метод ищет книгу по заданному параметру и возвращает эту книгу
        :param some_item: любой возможный аргумент для поиска(по имени, по автору, по году)
        :return: dict
        """
        my_lib = self.load_books()
        for inx, book in enumerate(my_lib):
            if isinstance(int(some_item), int):
                if some_item == book.get('year'):
                    return book
            else:
                if some_item == book.get('title'):
                    return book
                if some_item == book.get('author'):
                    return book
        return 'Такой книги не существует'

    def change_status(self, id: int, status: str) -> dict:
        """
        Этот метод меняет статус книги на новый и записывает в файл новые данные
        :param id: Айди книги
        :param status: новый статус для книги
        :return: dict
        """
        my_lib = self.load_books()
        for book in my_lib:
            if id == book.get('id'):
                book['status'] = status
                with open(self.path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(my_lib, ensure_ascii=False))
                return book

        return f'Книга с таким id: {id} не найденa'


def hello():
    print('Добро пожаловатьб чтобы вы хотели сделать?')


def running_app():
    print("Чтобы узнать нажмите:")
    print("(1) - о наличии книг в библиотеке")
    print("(2) - добавить книгу")
    print("(3) - найти книгу по автору, по названию или по году выпуска")
    print("(4) - удалить книгу")
    print("q - для выхода из приложения")
    my_lib = Library(FOLDER)
    while True:
        a = input('Введите что вы хотите сделать \n')
        match a:
            case '1':
                print(my_lib.load_books())
            case '2':
                title = input("Введите название книги: \n")
                author = input("Введите автора книги \n")
                try:
                    year = int(input("Введите год издания книги \n"))
                except ValueError as e:
                    print('Вы указали не верный формат года')
                else:
                    print(my_lib.add_book(title, author, year))
            case '3':
                attribute_search = input('Введите атрибут для поиска книги \n')
                print(my_lib.search_book(attribute_search))
            case '4':
                id_book = int(input('Введите id книги, которую вы хотите удалить'))
                print(my_lib.delete_book(id_book))
            case 'q' | 'й':
                print('Всего хорошего')
                break
            case _:
                print('Вы ввели не верное значение, попробуем все заново')
                running_app()




def main():
    hello()
    running_app()


if __name__ == '__main__':
    main()
