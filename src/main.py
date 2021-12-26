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


def main():
    while (1):
        print(
            'Do You Want To Search For the Book: Enter "Search" "View" "Delete" "Exit" '
        )
        flag = input(
        )  # user input options     "Search" "View" "Delete" "Exit"
        if flag.lower() == "exit":
            break
        if flag.lower() not in [
                "search", "view", "delete", "exit"
        ]:  # checking if user has inputted the correct option
            print('Invalid Command')
            continue
        else:
            pass

        if flag.lower() == 'search':
            ph = input(
                'Enter the Keyword to Search You Will get Title,publisher,author'
            )
            get = get_data(
                ph)  # calling get_data funct to get book list from google api
            my = save(
                get
            )  # calling save funct to save books that has be retrived by api
            print('Do you want to add Book in Reading List Enter : yes or no')
            ''' while loop to ask user if he/she 
                wants to add more books in reading list.
            '''
            while 1:
                y_n = input()
                if y_n.lower() == 'yes':
                    book_no = int(input('Enter Book No'))
                    if book_no > 5:
                        print('Your are Exceeding the Book Fetched')
                        print('Do You want to Add more Book')
                        continue
                    save_fav(my, book_no)
                    print('Do You want to Add more Book')
                elif y_n.lower() == 'no':
                    break
                else:
                    print('Invalid Input')

        # this is to check if user has input view i.e to he want to see his reading list
        if flag.lower() == 'view':
            display(myList)  # calling display to print mylist
        if flag.lower() == 'delete':
            print(f'No of books in Reading List is {len(myList)}')
            if len(myList) > 0:
                index = int(input("Enter the Index of Book to delete"))
                delete(
                    index
                )  # calling delete function to delete books from reading list by giving parameter i.e index