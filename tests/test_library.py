import os.path
import pytest
import tempfile
from main import print_pretty_table, Book, Library





class TestLibary:
    @pytest.fixture(scope='session')
    def temp_library_file(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        yield temp_file.name
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
    def test_add_book(self, temp_library_file):
        with Library(temp_library_file) as lib:
            lib.add_book('Детство', 'Л.Н. Толстой', 2000)
            assert len(lib.library) == 1
            assert lib.library[0].title == 'Детство'

    def test_delete_book(self, temp_library_file):
        with Library(temp_library_file) as lib:
            lib.delete_book(1)
            assert len(lib.library) == 0