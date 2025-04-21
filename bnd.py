import mysql.connector
from mysql.connector import Error
from sendEmail import *
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import socket
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = "june12006",
    database = "neuread"
)

mycursor = db.cursor(buffered=True)

mycursor.execute("USE neuread")
def getUserInfo(RFID):
    # Secure query to fetch user info
    mycursor.execute("SELECT * FROM users WHERE RFID = %s;", (RFID,))
    userInfo = mycursor.fetchall()

    # Secure query to fetch borrowed books
    mycursor.execute(
        "SELECT Book_ID, Date_Borrowed, Deadline FROM borrowed_books WHERE RFID = %s AND Date_returned IS NULL;",
        (RFID,),
    )
    userBorrowedBooks = mycursor.fetchall()

    books = []
    for i in userBorrowedBooks:  # Loop through each borrowed book
        mycursor.execute("SELECT Title, Author, Book_Cover FROM books WHERE Book_ID = %s;", (i[0],))  # ✅ Use i[0] instead of userBorrowedBooks[0][0]
        book = mycursor.fetchone()  # ✅ Use fetchone() instead of fetchall()
        books.append(book)

    return userInfo, userBorrowedBooks, books

def searchBooks(column, ID, nthTo, nthFrom):
    mycursor.execute(f"SELECT Book_ID, Book_Cover, Title, Availability FROM books WHERE {column} LIKE %s LIMIT %s OFFSET %s", (f"%{ID}%", nthTo, nthFrom))
    return mycursor.fetchall()

def searchBookID(bookID):
    mycursor.execute(f"SELECT Title, Author, Description, Availability, Book_Cover, Genre, Year_Publication, Book_Address FROM books WHERE Book_ID = {bookID};")
    return mycursor.fetchall()
def searchBookIDtoDelete(bookID):
    mycursor.execute(f"SELECT Title, Author, Description, Availability, Genre, Year_Publication, Book_Address FROM books WHERE Book_ID = {bookID};")
    result = mycursor.fetchone()
    if result:
        return {
            "Title": result[0],
            "Author": result[1],
            "Description": result[2],
            "Availability": result[3],
            "Genre": result[4],
            "Year_Publication": result[5],
            "Book_Address": result[6]
        }
    return result
def showGenreBooks(genre, nthFrom, nthTo):
    mycursor.execute("SELECT Book_ID, Book_Cover, Title, Availability  FROM books WHERE Genre = %s LIMIT %s OFFSET %s", (genre, nthTo, nthFrom))
    return mycursor.fetchall()

def showBorrowHistory(RFID, nthTo, nthFrom):
    mycursor.execute(
        "SELECT Book_ID, Date_Borrowed, Date_returned FROM borrowed_books WHERE RFID = %s AND `Date_returned` IS NOT NULL LIMIT %s OFFSET %s", 
        (RFID, nthTo, nthFrom)
    )
    
    items = mycursor.fetchall()  # Fetch borrowing history
    
    allBooks = []
    for book_id, date_borrowed, date_returned in items:
        mycursor.execute("SELECT Title, Author, Book_Cover FROM books WHERE book_ID = %s", (book_id,))
        book_info = mycursor.fetchone()  # Fetch one book's info
        if book_info:  # If book info is found, combine data
            title, author, book_cover = book_info
            allBooks.append([book_cover, title, author, date_borrowed, date_returned, book_id])
    return allBooks
def penalty(RFID, num):
    mycursor.execute("SELECT Penalty FROM users WHERE RFID = %s", (RFID,))
    penalty = mycursor.fetchone()[0]
    if penalty != num:
        mycursor.execute("UPDATE users SET Penalty = %s WHERE RFID = %s", (num, RFID))
        db.commit()
def emailPenalty(RFID):
    mycursor.execute("SELECT Email FROM users WHERE RFID = %s", (RFID,))
    gmail = mycursor.fetchone()[0]
    mycursor.execute("""
    SELECT 
        Date_Borrowed,
        Book_Title,
        DATEDIFF(CURDATE(), Date_Borrowed) AS Days_Borrowed
    FROM 
        borrowed_books 
    WHERE 
        RFID = %s AND Date_returned IS NULL;
""", (RFID,))
    result = mycursor.fetchall()
    for deadline, book_title, days in result:
        print(f"Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
        print(f"Gmail: {gmail}")
        print(f"Book Title: {book_title}")
        print(f"Days: {days}")
        print("-" * 40)
        send_Penalty_Info(gmail, deadline, book_title, days)
    print(result)
def showGenres(nthTo, nthFrom):
    mycursor.execute("SELECT DISTINCT `Genre` FROM books LIMIT %s OFFSET %s", (nthTo, nthFrom))
    return mycursor.fetchall()

def adminCheck(RFID):
    mycursor.execute("SELECT Email FROM users WHERE RFID = %s", (RFID,))
    result = mycursor.fetchone()

    mycursor.fetchall()  # Ensures all remaining results are cleared, preventing "Unread result found"
    
    return result is not None and result[0] == "Admin"
def addBorrowBook(RFID, Book_ID, Date_Borrowed, Deadline, Date_returned):
    mycursor.execute("SELECT Name FROM users WHERE RFID = %s", (RFID))
    Name = mycursor.fetchone()
    mycursor.execute("SELECT Title FROM books WHERE Book_ID = %s", (Book_ID))
    Title = mycursor.fetchone()
    mycursor.execute("INSERT INTO borrowed_books (RFID, Borrower_Name, Book_ID, Book_Title, Date_Borrowed, Deadline, Date_returned) VALUES (%s, %s, %s, %s, %s, %s, %s)", (RFID, Name, Book_ID, Title, Date_Borrowed, Deadline, Date_returned))
    mycursor.execute(
        "UPDATE books SET availability = 0 WHERE Book_ID = %s",
        (Book_ID,)
    )
    db.commit()
    
    #Mag e-email na
    mycursor.execute("SELECT Email FROM users WHERE RFID = %s;", (RFID,))
    borrowerEmail = mycursor.fetchall()[0][0]

    mycursor.execute("SELECT Title, Author FROM books WHERE Book_ID = %s;", (Book_ID,))
    title, author = mycursor.fetchall()[0]

    send_Borrow_Info(borrowerEmail, title, author, Date_Borrowed, Deadline)

def returnBook(RFID, Book_ID, Date_returned):
    # Update the borrowed_books table to set Date_returned where RFID and Book_ID match
    mycursor.execute(
        "UPDATE borrowed_books SET Date_returned = %s WHERE RFID = %s AND Book_ID = %s",
        (Date_returned, RFID, Book_ID)
    )

    # Update the books table to set availability back to 1 (available)
    mycursor.execute(
        "UPDATE books SET availability = 1 WHERE Book_ID = %s",
        (Book_ID,)
    )
    
    # Commit both operations
    db.commit()
def showWhoToEmail():
    listGmail = []

    borrow_IDs = WhoToPenalize()

    for row in borrow_IDs: 
        rfid = row[0]  # Assuming RFID is in the second column
        # Secure query to fetch email
        mycursor.execute("SELECT DISTINCT Email FROM users WHERE RFID = %s;", (rfid,))
        result = mycursor.fetchone()  # Get the single email result
        mycursor.execute("SELECT Title, Deadline FROM borrowed_books WHERE RFID = %s; and Date_returned is NULL", (rfid,))
        title, deadline = mycursor.fetchall()[0]
        if result:  # Ensure result is not None
            listGmail.append((result[0], title, deadline))  # Append the email to the list
            db.commit()

    for email in listGmail:
        send_Deadline_Info(email)
    return listGmail
def WhoToPenalize():
    mycursor.execute("SELECT RFID FROM borrowed_books WHERE date_returned IS NULL AND Deadline <= CURDATE() AND Borrower_Name IS NOT NULL;")
    borrow_IDs = mycursor.fetchall()
    print(borrow_IDs)
    for row in borrow_IDs:
        rfid = row[0]  # Assuming RFID is in the second column
        print("PENALIZE: ", rfid)
        penalty(rfid, 1)
    return borrow_IDs
def getUserAndBookNum():
        # Query 1: Count all rows in the table
        mycursor.execute("SELECT COUNT(*) FROM users;")
        total_UserRows = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM books;")
        total_BookRows = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM users where Penalty = '1';")
        total_PenaltyRows = mycursor.fetchone()[0]
        return total_UserRows, total_BookRows, total_PenaltyRows

def BnRcount_rows(start_date, end_date):
    query = """
    SELECT COUNT(*) 
    FROM borrowed_books 
    WHERE Date_borrowed BETWEEN %s AND %s;
    """
    mycursor.execute(query, (start_date, end_date))
    filtered_BorrowData = mycursor.fetchone()[0]

    query = """
    SELECT COUNT(*) 
    FROM borrowed_books 
    WHERE Date_returned BETWEEN %s AND %s;
    """
    mycursor.execute(query, (start_date, end_date))
    filtered_ReturnedData = mycursor.fetchone()[0]

    return filtered_BorrowData, filtered_ReturnedData
def export_to_excel(start_date, end_date):
    query = """
    SELECT * FROM borrowed_books
    WHERE Date_borrowed BETWEEN %s AND %s;
    """
    mycursor.execute(query, (start_date, end_date))
    
    # Fetch data
    rows = mycursor.fetchall()
    
    # Get column names
    column_names = [desc[0] for desc in mycursor.description]

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    # Define file name
    filename = "borrowed_books_export.xlsx"

    # Export to Excel (in the same directory as the script)
    df.to_excel(filename, index=False)

    return filename

def send_email_with_attachment(RECIPIENT_EMAIL, start_date, end_date):
    # Email Credentials
    SENDER_EMAIL = "neuread.neuis@gmail.com"
    SENDER_PASSWORD = "agiv uhqq tlhg sjre"

    subject = "Borrowed Books Data Export"
    body = f"Here is the exported data of borrowed books from {start_date} to {end_date}."

    # Export the data
    filename = export_to_excel(start_date, end_date)
    print(filename)
    if filename is None:
        print("❌ Failed to export data. Email not sent.")
        return

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach the Excel file
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filename)}")
    msg.attach(part)

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()

        print(f"✅ Email with attachment sent successfully to {RECIPIENT_EMAIL}!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
def ifTheyHaveTheBook(bookID, RFID):
    mycursor.execute("select RFID from borrowed_books where book_ID = %s and Date_returned IS NULL", (bookID,))
    borrowerRFID = mycursor.fetchone()
    print(RFID)
    if borrowerRFID:
        print("RFID of user: ", RFID, " RFID OF THE BORROWER: ", borrowerRFID[0])
        if RFID == borrowerRFID[0]:
            print("true")
            return True
        else:
            print("false")
            return False
    print("wala siyang record")
def ifTheyExceedBorrow(RFID):
    mycursor.execute("SELECT COUNT(*) FROM borrowed_books WHERE RFID = %s AND Date_returned IS NULL", (RFID,))
    borrowed_count = mycursor.fetchone()[0]

    return borrowed_count >= 2
def checkPenalty(RFID):
    mycursor.execute("SELECT Penalty FROM users WHERE RFID = %s", (RFID,))
    try:
        penalty = mycursor.fetchone()[0]
        if penalty == 1:
            return True
        else:
            return False
    except:
        return False
def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Returns True if internet is connected, otherwise False.
    Default tries to reach Google's DNS at 8.8.8.8
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def insert_book(data):
    try:
        if db.is_connected():
            cursor = db.cursor()

            try:
                # Read the image file
                with open(data['Book_Cover'], 'rb') as f:
                    image_blob = f.read()
            except FileNotFoundError:
                print(f"Error: The file '{data['Book_Cover']}' was not found.")
                return
            except Exception as e:
                print(f"Error reading the image file: {e}")
                return

            # Prepare the SQL query
            sql = ("INSERT INTO books (Book_ID, Title, Author, Description, Availability, "
                   "Book_Cover, Genre, Year_Publication, Book_Address) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            values = (
                data['Book_ID'],
                data['Title'],
                data['Author'],
                data['Description'],
                data['Availability'],
                image_blob,
                data['Genre'],
                data['Year_Publication'],
                data['Book_Address']
            )

            try:
                # Execute the query and commit the transaction
                cursor.execute(sql, values)
                db.commit()
                print("Book inserted successfully.")
            except mysql.connector.Error as e:
                print(f"MySQL Error: {e}")
                db.rollback()  # Rollback in case of error
            except Exception as e:
                print(f"Error executing the query: {e}")
                db.rollback()  # Rollback in case of error

            # Close the cursor
        else:
            print("Error: Unable to connect to the database.")

    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
    except Exception as e:
        print(f"General error: {e}")
def delete_book_by_ID(Book_ID):
    try:
        mycursor.execute("DELETE FROM books WHERE Book_ID = %s", (Book_ID,))
        db.commit()
        affected_rows = mycursor.rowcount
        return affected_rows
    except mysql.connector.Error as err:
        raise err
print(adminCheck("0010542281"))