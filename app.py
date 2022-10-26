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
        \r the price formal should look like 12.99
        \r press enter to try again
        \r**************************''')
        return
    return return_price



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
            pass
        elif choice == '4':
            pass
        else:
            print('GOODBYE')
            app_running=False 



if __name__=='__main__':
    Base.metadata.create_all(engine)
    app()
    add_csv()
    