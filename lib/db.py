import sqlite3 # Import the sqlite3 module to work with SQLite databases
import datetime # Import the datetime module for date and time handling
import ast # Import the ast module to convert strings to Python data structures

class DB:
    
    def create_db(self):
        # Books table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS book
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name CHAR(100) NOT NULL,
                            publisher CHAR(100) NOT NULL,
                            writer CHAR(100) NOT NULL,
                            subject CHAR(100) NOT NULL,
                            year CHAR(10) NOT NULL,
                            published CHAR(10) NOT NULL,
                            number CHAR(10) NOT NULL,
                            price CHAR(10) NOT NULL
                          );
                          ''')
        # Loan table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS loan
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name CHAR(100) NOT NULL,
                            user_id CHAR(100) NOT NULL,
                            books CHAR(100) NOT NULL,
                            status CHAR(10) NOT NULL,
                            date DATE NOT NULL
                          );
                          ''')
        # Personal info table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS info
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            shop_name CHAR(100) NOT NULL,
                            shop_add CHAR(200) NOT NULL,
                            shop_phone CHAR(100) NOT NULL,
                            name CHAR(100) NOT NULL,
                            email CHAR(10) NOT NULL
                          );
                          ''')
        # Sell table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS sell
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id CHAR(100) NOT NULL,
                            number CHAR(100) NOT NULL,
                            price CHAR(100) NOT NULL,
                            user_id CHAR(100) NOT NULL,
                            user_name CHAR(100) NOT NULL
                          );
                          ''')
    
    # Connect to the SQLite database file 'libdb.db
    def __init__(self):
        self.conn = sqlite3.connect('libdb.db')
        self.create_db()
    
    # Query the loan table to retrieve all rows where user_id matches the provided user_id and the status is '0' (meaning the book is currently on loan)
    def search_loan(self, user_id):
        cursor = self.conn.execute("SELECT * FROM loan WHERE user_id='{user_id}' AND status='0';".format(user_id=user_id))
        out = []
        

        for row in cursor:
            loan = []
            for item in row:
                loan.append(item)
            out.append(loan)
        return out
    
    # Update the loan table by setting the status to '1' (returned) for the row with the given id
    def change_loan_status(self, id):
        self.conn.execute("UPDATE loan SET status='1' WHERE id={id};".format(id=id))
    
    # Query the loan table to retrieve the 'books' column where the 'id' column matches the provided 'id'
    def get_loan_cart(self, id):
        cursor = self.conn.execute("SELECT books FROM loan WHERE id={id}".format(id=id))
        for row in cursor:
            return ast.literal_eval(row[0])
    
    # Used to retrieve data from the loan table with a status of '0'
    def get_all_loan(self):
        cursor = self.conn.execute("SELECT * FROM loan WHERE status='0';")
        out = []
        for row in cursor:
            loan = []
            for item in row:
                loan.append(item)
            out.append(loan)
        return out
    
    #  The loan_book function takes three arguments: id (user ID), name (user name), and cart (a list or collection of books to be loaned).
    def loan_book(self, id, name, cart):
        db_string = "INSERT INTO loan (name, user_id, books, status, date) VALUES (?,?,?,?,?);"
        data = (name, id, str(cart), '0', str(datetime.datetime.now()))
        cursor = self.conn.cursor()
        cursor.execute(db_string, data)
        self.conn.commit()
        cursor.close()
    
    #  The sell_book function takes three arguments: id (user ID), name (user name), and cart (a list or collection of books to be sold).
    def sell_book(self, id, name, cart):
        for i in range(len(cart)):
            db_string = "INSERT INTO sell (book_id, number, price, user_id, user_name) VALUES (?,?,?,?,?);"
            data = (cart[i]['id'], cart[i]['number'], cart[i]['price'], id, name)
            curser = self.conn.cursor()
            curser.execute(db_string, data)
            self.conn.commit()
            curser.close()
    
    # The add_book function takes eight arguments: name (book name), publisher, writer (author or writer), subject (subject or category), year (publication year), published (publication status, usually 0 or 1), number (number of copies available), and price.
    def add_book(self, name, publisher, writer, subject, year, published, number, price):
        db_string = "INSERT INTO book (name, publisher, writer, subject, year, published, number, price) VALUES (?,?,?,?,?,?,?,?);"
        data = (name, publisher, writer, subject, year, published, number, price)
        curser = self.conn.cursor()
        curser.execute(db_string, data)
        self.conn.commit()
        curser.close()
    
    # Takes nine arguments: id (book ID), name (new book name), publisher, writer (new author or writer), subject (new subject or category), year (new publication year), published (new publication status, usually 0 or 1), number (new number of copies available), and price (new price).
    def edit_book(self, id, name, publisher, writer, subject, year, published, number, price):
        db_string = "UPDATE book SET name=?, publisher=?, writer=?, subject=?, year=?, published=?, number=?, price=? WHERE id=?;"
        data = (name, publisher, writer, subject, year,published, number, price, id)
        cursor = self.conn.cursor()
        cursor.execute(db_string, data)
        self.conn.commit()
        cursor.close()
    
    # The del_book function takes a single argument: id, which is the ID of the book to be deleted.
    def del_book(self, id):
        cursor = self.conn.execute("DELETE FROM book WHERE id={id};".format(id=id))
        cursor.close()
        
    # The count_book function is a method of a class that has a database connection (self.conn).
    def count_book(self):
        cursor = self.conn.execute('SELECT Count(*) FROM book;')
        number = 0
        for row in cursor:
            number = row[0]
        cursor.close()
        return int(number)
      
    # The select_all_book function is a method of a class that has a database connection (self.conn).
    def select_all_book(self):
        cursor = self.conn.execute('SELECT * FROM book')
        out = []
        for row in cursor:
            book = []
            book.append(row[0]) # id
            book.append(row[1]) # name
            book.append(row[2]) # publisher
            book.append(row[3]) # writer
            book.append(row[4]) # subject
            book.append(row[5]) # year
            book.append(row[6]) # published
            book.append(row[7]) # number
            book.append(row[8]) # price
            out.append(book)
        cursor.close()
        return out
    
    # The search_book function takes a single argument werb, which is the search term.
    def search_book(self, werb):
        
        # Remove leading and trailing whitespaces, and split the search term into individual words
        werb = werb.rstrip().lstrip().split(' ')
        
        # Initialize the 'like' string with a wildcard '%' for pattern matching
        like = '%'
        
        # Iterate over each word in the search term
        for i in range(len(werb)):
        
        # Append the word with wildcards before and after to the 'like' string
            like += '{w}%'.format(w=werb[i])
        cursor = self.conn.execute("SELECT * FROM book WHERE name LIKE '{like}';".format(like=like))
        out = []
        for row in cursor:
            book = []
            book.append(row[0])
            book.append(row[1])
            book.append(row[2])
            book.append(row[3])
            book.append(row[4])
            book.append(row[5])
            book.append(row[6])
            book.append(row[7])
            book.append(row[8])
            out.append(book)
        cursor.close()
        return out
      
    # The select_by_id function takes a single argument id, which is the ID of the book to be selected.
    def select_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM book WHERE id={id};'.format(id=id))
        out = []
        for row in cursor:
            book = []
            book.append(row[0])
            book.append(row[1])
            book.append(row[2])
            book.append(row[3])
            book.append(row[4])
            book.append(row[5])
            book.append(row[6])
            book.append(row[7])
            book.append(row[8])
            out.append(book)
        cursor.close()
        return out