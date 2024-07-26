from unittest import TestCase, main

import os
from main import Library


class TestLibrary(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_path = 'test_lib.json'
        cls.library = Library(path=cls.test_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.test_path):
            os.remove(cls.test_path)

    def setUp(self):
        self.library.__enter__()

    def tearDown(self):
        self.library.__exit__(None, None, None)

    def test_add_book(self):
        # Test adding a new book
        self.library.add_book('Book_1', 'Author_1', 2024)
        self.assertEqual(len(self.library.library), 1)
        self.assertEqual(self.library.library[0].title, 'Book_1')
        self.assertEqual(self.library.library[0].author, 'Author_1')
        self.assertEqual(self.library.library[0].year, 2024)

    def test_delete_book(self):
        # Test deleting an existing book
        self.library.add_book('Book_2', 'Author_2', 2024)
        self.library.delete_book(2)
        self.assertEqual(len(self.library.library), 2)

    def test_change_status(self):
        # Test changing the status of a book
        self.library.add_book('Book_3', 'Author_3', 2024)
        self.library.change_status(1, 'выдана')
        self.assertEqual(self.library.library[0].status, 'выдана')

    def test_search_book_by_title(self):
        # Test searching a book by title
        self.library.add_book('Book_4', 'Author_4', 2024)
        result = self.library.search_book('Book_4')
        self.assertIn('Book_4', result)

    def test_search_book_by_author(self):
        # Test searching a book by author
        self.library.add_book('Book_5', 'Author_5', 2024)
        result = self.library.search_book('Author_5')
        self.assertIn('Author_5', result)

    def test_search_book_by_year(self):
        # Test searching a book by year
        self.library.add_book('Book_6', 'Author_6', 2024)
        result = self.library.search_book(2024)
        self.assertIn('2024', result)

    def test_load_books(self):
        # Test loading books from file
        self.library.add_book('Book_7', 'Author_7', 2024)
        self.library.__exit__(None, None, None)

        new_library = Library(path=self.test_path)
        new_library.__enter__()

        self.assertEqual(len(new_library.library), 3)
        self.assertEqual(new_library.library[0].title, 'Book_1')
        self.assertEqual(new_library.library[0].author, 'Author_1')
        self.assertEqual(new_library.library[0].year, 2024)


if __name__ == '__main__':
    main()
