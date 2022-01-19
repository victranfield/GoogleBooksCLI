import requests
import re

def get_data(phrase):
    if len(phrase) >= 10000:
        print("your input value is too long, please enter a smaller value")
        return None
    # handling abnormally long string
    try:
        response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={phrase}", timeout=5)  # making request
        # f"https://httpbin.org/delay/10", timeout=5) # making request
        #https://www.googleapis.com/books/v1/volumes?q={phrase}"
        data = response.json(
        )
    except Exception:
        data = None
        print("connection to server not made")
    return data  # return data fetched in json
    # handling connection errors


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
def save_fav(fav, no, myList):
    if fav[no - 1] not in myList:  # checking if book is already present or not
        myList.append(fav[no - 1])
        display(myList)  # simply calling display to shop book details
    else:
        print('Book Already Present')


# used for deleting books in the reading list
def delete(index, myList):
    if index <= len(myList):
        myList.pop(
            index - 1
        )  # used to delete element in list (myList i.e is reading List)
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

def add_books(my, myList):
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
            save_fav(my, book_no, myList)
            print('Do You want to Add more Book')
        elif y_n.lower() == 'no':
            break
        else:
            print('Invalid Input')

def search_book(myList):
    ph = input(
        'Enter the Keyword to Search You Will get Title,publisher,author'
    )
    # matched = re.match("[A-Za-z0-9 ]*", ph)
    # print(matched)
    # is_match = bool(matched)
    if not re.match("[A-Za-z0-9 ]+", ph):
    # if input is not is_match:
    # guarding against inputting random strings
        print("Please provide a valid word to search with")
        return
    data = get_data(
        ph)  # calling get_data funct to get book list from google api
    if not data or "items" not in data:
        # if item is not present, return message to user asking for valid input
        print("Please provide a value to search with")
        return
        # TODO - direct user to keyword step, would need to be broken into smaller parts
    my = save(
        data
    )  # calling save funct to save books that have be retrived by api
    add_books(my, myList)

def delete_book(myList):
    print(f'No of books in Reading List is {len(myList)}')
    if len(myList) > 0:
        try:
            index = int(input("Enter the Index of Book to delete"))
            delete(
            index, myList
            )
        except ValueError:
            print("Give a numeric value")
        #checking that numeric string is entered when deleting a book


def main(myList):
    while (1):
        print(
            'Do You Want To Search For the Book: Enter "Search" "View" "Delete" "Exit" '
        )
        #
        try:
            flag = input(
        )  # user input options     "Search" "View" "Delete" "Exit"
        #waiting for input
        #keyboard interrupt - when control C is pressed
        except KeyboardInterrupt:
            print("The application has been cancelled")
            break
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
            search_book(myList)

        # this is to check if user has input view i.e to able to see their reading list
        if flag.lower() == 'view':
            display(myList)  # calling display to print mylist
        if flag.lower() == 'delete':
            delete_book(myList)


if __name__ == '__main__':
    main([])
