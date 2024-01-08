import sqlite3

def initialize_database():
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        quantity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_number TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lend_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        book_id INTEGER,
        date_borrowed DATE,
        date_returned DATE,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    )
    """)

    connection.commit()
    connection.close()

def add_book(title, author, quantity):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)", (title, author, quantity))

    connection.commit()
    connection.close()

def retrieve_books(search=None):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    if search:
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search + '%', '%' + search + '%'))
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()
    return books

def update_book(book_id, title, author, quantity):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE books SET title=?, author=?, quantity=? WHERE id=?", (title, author, quantity, book_id))

    connection.commit()
    connection.close()

def delete_book(book_id):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))

    connection.commit()
    connection.close()

def add_student(name, roll_number, email):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO students (name, roll_number, email) VALUES (?, ?, ?)", (name, roll_number, email))

    connection.commit()
    connection.close()

def student_list():
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()
    return students

def lend_book(student_id, book_id, date_borrowed):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO lend_records (student_id, book_id, date_borrowed) VALUES (?, ?, ?)", (student_id, book_id, date_borrowed))
    lend_id= execute("SELECT LAST (id) FROM lend_records;  ")
    connection.commit()
    connection.close()

def return_book(lend_record_id, date_returned):
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE lend_records SET date_returned=? WHERE id=?", (date_returned, lend_record_id))

    connection.commit()
    connection.close()


def login():
    connection = sqlite3.connect("myLibrary.db")
    cursor = connection.cursor()
    print("\nLibrary Management System\n")
    print("1. Librarian Login")
    print("2. Student Login")
    print("0. Exit")
    log= input(" enter your choice: ")
    if(log =='1'):
        finLogin='1'
    elif(log=='2'):
        nameChk= input("Enter Student Name: ")
        idChk= input("Enter Student id: ")
        cursor.execute("select count(*) from students where name= ? AND id= ?",(nameChk,idChk))
        count=cursor.fetchone()[0]
        if(count>=1):
            finLogin='2'
        else:
            print("Student not found")
            finLogin="-1"
    elif(log=='0'):
        finLogin='0'
    else:
        print("Invalid choice")
        finLogin="-1"
    
    connection.close()
    return finLogin

def choices(chk):
    if (chk=='1'):
        print("1. Add Book")
        print("2. Book List")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Add Student")
        print("6. Students List")
        print("7. Lend Books")
        print("8. Return Books")
        print("0. Exit")
        choice= input("Enter your choice: ")
        return choice

    elif(chk=='2'):
        print("1. Retrieve Books")
        print("2. Take Books")
        print("3. Return Books")
        print("0. Exit")
        choice= input("Enter your choice: ")
        if(choice=='2'):
            return '7'
        elif(choice=='1'):
            return '2'
        elif choice=='3':
            return '8'
        else:
            return choice
        

def main():
    initialize_database()
    while True:
        log=login()

        if log=='1' or log=='2':
            while True:
                choice= choices(log)
                if choice == '0':
                    break
                elif choice == '1':
                    title = input("Enter book title: ")
                    author = input("Enter book author: ")
                    quantity = int(input("Enter quantity: "))
                    add_book(title, author, quantity)
                    print("Book added successfully!")
                elif choice == '2':
                    search = input("Enter search keyword (press Enter to retrieve all): ")
                    books = retrieve_books(search)
                    print("\nBooks in the library:")
                    for book in books:
                        print(book)
                elif choice == '3':
                    book_id = int(input("Enter book ID to update: "))
                    title = input("Enter new title: ")
                    author = input("Enter new author: ")
                    quantity = int(input("Enter new quantity: "))
                    update_book(book_id, title, author, quantity)
                    print("Book updated successfully!")
                elif choice == '4':
                    book_id = int(input("Enter book ID to delete: "))
                    delete_book(book_id)
                    print("Book deleted successfully!")
                elif choice == '5':
                    name = input("Enter student name: ")
                    roll_number = input("Enter student roll number: ")
                    email = input("Enter student email: ")
                    add_student(name, roll_number, email)
                    print("Student added successfully!")
                elif choice == '6':
                    students = student_list()
                    print("\nStudents in the system:")
                    for student in students:
                        print(student)
                elif choice == '7':
                    student_id = int(input("Enter student ID: "))
                    book_id = int(input("Enter book ID: "))
                    date_borrowed = input("Enter date borrowed (YYYY-MM-DD): ")
                    lend_id=lend_book(student_id, book_id, date_borrowed)
                    print("Book lent successfully!\n Lend Id:")
                    print(lend_id)
                elif choice == '8':
                    lend_record_id = int(input("Enter lend record ID: "))
                    date_returned = input("Enter date returned (YYYY-MM-DD): ")
                    return_book(lend_record_id, date_returned)
                    print("Book returned successfully!")
                else:
                    print("Invalid choice. Please try again.")
        elif(log=='-1'):
            continue
        else:
            break
    print("Thank You")
                


if __name__ == "__main__":
    main()                