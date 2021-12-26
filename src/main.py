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