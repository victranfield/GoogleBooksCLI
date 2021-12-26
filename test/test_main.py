import unittest
from unittest import mock
from unittest.mock import patch
from io import StringIO

from src.main import display, save_fav, delete, main, save

book_list = []
myList = []
mock_stdout = patch('sys.stdout', new_callable=StringIO)

class TestDisplay(unittest.TestCase):
    @mock_stdout
    def test_empty(self, stdout):
        '''Test displaying an empty reading list.'''
        display([])
        output = stdout.getvalue().strip()
        self.assertEqual(output, 'Reading List Empty')

    @mock_stdout
    def test_1_book(self, stdout):
        '''Test displaying a list with only one book.'''
        books = [{'title': 'Hello', 'publisher': 'John', 'author': 'Jane'}]
        display(books)
        output = stdout.getvalue().strip()
        self.assertEqual(
            output,
            '***\nBook 1:\nTitle: Hello\npublisher: John\nauthor: Jane')

    @mock_stdout
    def test_multiple(self, stdout):
        '''Test displaying a list with multiple books.'''
        books = [{
            'title': 'Hello',
            'publisher': 'John',
            'author': 'Jane'
        }, {
            'title': 'Harry Potter',
            'publisher': 'J K Rowling',
            'author': 'J K Rowling'
        }]
        display(books)
        output = stdout.getvalue().strip()
        self.assertEqual(
            output,
            '***\nBook 1:\nTitle: Hello\npublisher: John\nauthor: Jane\n\n***\nBook 2:\nTitle: Harry Potter\npublisher: J K Rowling\nauthor: J K Rowling'
        )


class TestSaveFav(unittest.TestCase):
    @mock_stdout
    def test_add_book(self, stdout):
        '''Test adding a single book.'''
        global myList
        oldMyList = myList[:]
        myList = []
        save_fav([{
            'title': 'Harry Potter',
            'publisher': 'J K Rowling',
            'author': 'J K Rowling'
        }], 1)

        output = stdout.getvalue().strip()
        self.assertEqual(
            output,
            '***\nBook 1:\nTitle: Harry Potter\npublisher: J K Rowling\nauthor: J K Rowling'
        )
        myList = oldMyList[:]


class TestDelete(unittest.TestCase):
    @mock_stdout
    def test_delete_empty(self, stdout):
        '''Test deleting a book from an empty list.'''
        global myList
        oldMyList = myList[:]
        myList = []

        delete(1)
        output = stdout.getvalue().strip()
        self.assertEqual(output, 'Reading List Size Is lower Than give Index')

        myList = oldMyList[:]

class TestSave(unittest.TestCase):
    @mock_stdout
    def test_save_one(self, stdout):
        '''Test saving one book.'''
        data = {
            'items': [{
                'volumeInfo': {
                    'title': '1',
                    'authors': ['1'],
                    'publisher': '1'
                }
            }]
        }

        books = save(data)
        self.assertEqual(books, [{
            'title': '1',
            'publisher': '1',
            'author': '1'
        }])

    @mock_stdout
    def test_save_multiple(self, stdout):
        '''Test saving multiple books.'''
        data = {
            'items': [{
                'volumeInfo': {
                    'title': '1',
                    'authors': ['1'],
                    'publisher': '1'
                }
            }, {
                'volumeInfo': {
                    'title': '2',
                    'authors': ['2', 'Two'],
                    'publisher': '2'
                }
            }, {
                'volumeInfo': {
                    'title': '3',
                    'authors': ['3'],
                    'publisher': '3'
                }
            }]
        }

        books = save(data)
        self.assertEqual(books, [{
            'title': '1',
            'publisher': '1',
            'author': '1'
        }, {
            'title': '2',
            'publisher': '2',
            'author': '2, Two'
        }, {
            'title': '3',
            'publisher': '3',
            'author': '3'
        }])

    @mock_stdout
    def test_na(self, stdout):
        '''Test saving a book with missing fields.'''
        data = {'items': [{'volumeInfo': {}}]}
        books = save(data)
        self.assertEqual(books, [{
            'title': 'N/A',
            'publisher': 'N/A',
            'author': 'N/A'
        }])


class TestMain(unittest.TestCase):
    @mock_stdout
    def test_main_exit(self, stdout):
        '''Test exiting the program without doing anything.'''
        stdin = mock.builtins.input
        mock.builtins.input = lambda: 'exit'
        main()
        output = stdout.getvalue().strip()

        self.assertEqual(
            output,
            'Do You Want To Search For the Book: Enter "Search" "View" "Delete" "Exit"'
        )

        mock.builtins.input = stdin

    @mock_stdout
    def test_main_view(self, stdout):
        '''Test searching for a single book and exiting.'''
        stdin = mock.builtins.input
        inputs = ['search', 'a song of ice and fire', 'no', 'exit']

        mock.builtins.input = lambda _=None: inputs.pop(0)

        main()
        output = stdout.getvalue().strip()

        for value in [
                'Do You Want To Search For the Book: Enter "Search" "View" "Delete" "Exit"',
                'Book 1', 'Book 2', 'Book 3', 'Book 4', 'Book 5',
                'Do you want to add Book in Reading List Enter : yes or no'
        ]:
            self.assertIn(value, output)

        mock.builtins.input = stdin


if __name__ == '__main__':
    unittest.main()
