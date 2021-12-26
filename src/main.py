import requests

book_list = []
myList = []


def get_data(phrase):
    data = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={phrase}").json(
        )  # making request
    return data  # return data fetched in json


# display book Details
def display(dic):
    if dic == []:
        print('Reading List Empty')
        return
    n = 1
    for i in dic:
        print('***')
        print(f'Book {n}:')
        print('Title:', i['title'])
        print('publisher:', i['publisher'])
        print('author:', i['author'])
        print()
        n = n + 1

# saving book in reading List
def save_fav(fav, no):
    if fav[no - 1] not in myList:  # cheching if book is already present or not
        myList.append(fav[no - 1])
        display(myList)  # simply calling display to shop book details
    else:
        print('Book Already Present')


# used for deleting books in the reading list
def delete(index):
    if index <= len(myList):
        myList.pop(
            index - 1
        )  # used to delete element is list name myList i.e is reading List
        print('Book is Deleted')
    else:
        print('Reading List Size Is lower Than give Index')


# simply saving book details in a list of dictionary to use in future process
def save(data):
    book_list = []
    for i in data['items'][0:5]:
        volumeInfo = i['volumeInfo']
        book = {
            'title':
            volumeInfo['title'] if 'title' in volumeInfo else 'N/A',
            'publisher':
            volumeInfo['publisher'] if 'publisher' in volumeInfo else 'N/A',
            'author':
            ', '.join(volumeInfo['authors'])
            if 'authors' in volumeInfo else 'N/A'
        }
        book_list.append(book)
    display(book_list)
    return book_list
