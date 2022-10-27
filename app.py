from models import Base, session, Book, engine
import datetime
import csv
import time

def menu():
    while True:
        print('''
              \nPROGRAMMING BOOKS
              \r1) Add book
              \r2) View all books
              \r3) Find book
              \r4) Book analysis
              \r5) exit''')
        choice = input('What would you like to do?  ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else: input('''
                    \nPlease choose one of the options above.
                    \rHit enter to try again.''')


def submenu():
    while True:
        print('''
              \nPROGRAMMING BOOKS
              \r1) Edit
              \r2) Delete
              \r3) Return to menu''')
        choice = input('What would you like to do?  ')
        if choice in ['1', '2', '3']:
            return choice
        else: input('''
                    \nPlease choose one of the options above.
                    \rHit enter to try again.''')


def editmenu():
    while True:
        print(f'''
                \nSelect which you would like to edit:
                \r1) Title
                \r2) Author
                \r3) Price
                \r4) Publish date
                \r5) Return to menu''')
        ed_choice = input('What would you like to do?  ')
        if ed_choice in ['1', '2', '3', '4', '5']:
            return ed_choice
        else: input('''
                    \nPlease choose one of the options above.
                    \rHit enter to try again.''')



def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date=datetime.date(year, month, day)
    except ValueError:
        input('''
        \n ****** DATE ERROR ******
        \r the date format should look like October 25, 2017
        \r press enter to try again
        \r**************************''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_fl = float(price_str)
        return_price=int(price_fl * 100)
    except ValueError:
        input('''
        \n ****** PRICE ERROR ******
        \r the price format should look like 12.99
        \r press enter to try again
        \r**************************''')
        return
    return return_price


def clean_id(id_str, options):
    try:
        book_id=int(id_str)
    except ValueError:
        input('''
        \n ******* ID ERROR *******
        \r the ID format should be a number
        \r press enter to try again
        \r**************************''')
        return
    else: 
        if book_id in options:
            return book_id
        else:
            input(f'''
        \n ******* ID ERROR *******
        \r Options: {options} 
        \r press enter to try again
        \r**************************''')
            return


def edit(book, edit_choice): 
    if edit_choice == '1':
        if book.title == None:
            print(f'Currently this book has no title')
        else:
            print(f'Current Title: {book.title}')
        new_title = input('What would you like to change the title to?  ')
        return new_title
    elif edit_choice == '2':
        if book.author == None:
            print(f'Currently this book has no author')
        else:
            print(f'Current Author: {book.author}')
        new_author = input('What would you like to change the price to?  ')
        return new_author
    elif edit_choice == '3':
        if book.price == None:
            print(f'Currently this book has no price')
        else:
            print(f'Current price: {book.price/100}')
        new_price_error=True
        while new_price_error:
            new_price = input('What would you like to change the price to?  ')
            new_price=clean_price(new_price)
            if type(new_price) == int:
                new_price_error=False
        return new_price
    elif edit_choice == '4':
        if book.price == None:
            print(f'Currently this book has no price')
        else:
            print(f'Current date: {book.date_published.strftime("%B %d, %Y")}')
        new_date_error=True
        while new_date_error: 
            new_date = input('What would you like to change the published date to? (ex October 25, 2017)  ')
            new_date=clean_date(new_date)
            if type(new_date) ==  datetime.date:
                new_date_error=False
        return new_date


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                print(row)
                title = row[0]
                author = row[1]
                date_published = clean_date(row[2])
                price = clean_price(row[3])
                new_book=Book(title=title, author=author, date_published=date_published, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice= menu()
        if choice == '1':
            title=input('Title:  ')
            author=input('Author: ')
            date_error=True
            while date_error: 
                date_published=input('Date published (ex October 25, 2017):  ')
                date_published=clean_date(date_published)
                if type(date_published) ==  datetime.date:
                    date_error=False
            price_error=True
            while price_error:
                price=input('Price:  ')
                price=clean_price(price)
                if type(price) == int:
                    price_error=False
            new_book = Book(title=title, author=author, date_published=date_published, price=price)
            session.add(new_book)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.date_published} | {book.price}')
            input('Press enter to return to menu')
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \n id options: {id_options}
                    \r Choose a Book:  ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author}
                \r Published in {the_book.date_published}
                \r Price: {the_book.price}''')
            subchoice = submenu()
            if subchoice == '1':
                edit_choice = editmenu()
                if edit_choice == '1':
                    the_book.title = edit(the_book, '1')
                    print(f'The Title has been updated to {the_book.title}')
                elif edit_choice == '2':
                    the_book.author = edit(the_book, '2')
                    print(f'Author of {the_book.title} has been updated to {the_book.author}')
                elif edit_choice == '3':
                    the_book.price = edit(the_book, '3')
                    print(f'Price of {the_book.title} has been updated to {the_book.price}')
                elif edit_choice == '4':
                    the_book.date_published = edit(the_book, '4')
                    print(f'Publish date of {the_book.title} has been updated to {the_book.date_published.strftime("%B %d, %Y")}')
                session.commit()
                time.sleep(1.5)
            elif subchoice == '2':
                sure = input(f'''
                                \n Are you sure you want to delete {the_book.title}? 
                                \rtype Y to confirm ''')
                if sure == 'Y':
                    session.delete(the_book)
                    session.commit()
                    print('BOOK DELETED')
                    time.sleep(1.5)
        elif choice == '4':
            pass
        else:
            print('GOODBYE')
            app_running=False 



if __name__=='__main__':
    Base.metadata.create_all(engine)
    app()
    # add_csv()
    # edit(session.query(Book).filter(Book.id == '4').first(), '1')
    # p=(clean_price(21.24))
    # print(p)
  
    