import tkinter as tk
from datetime import datetime
from tkinter import *
from bnd import *
import pytz
import customtkinter as ctk
from PIL import Image, ImageTk
import io
import threading
from Book_profile import *
# GLOBAL VARIABLES HERE
showBook = 0
book_buttons = []

def Main_history_page(content, RFID):
    global showBook
    for widget in content.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    showBook = 0
    history_page = tk.Frame(content)
    history_page.place(relx=0, rely=0, relwidth=1, relheight=1)
    ww = history_page.winfo_screenwidth()
    wh = history_page.winfo_screenheight()
    time_border = ctk.CTkFrame(history_page, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(history_page, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05)

    def update_date():
        ph_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.now(ph_timezone)
        formatted_date = current_time.strftime("%B %d, %Y")
        formatted_time = current_time.strftime("%I:%M %p")
        date_label.configure(text=formatted_date)
        time_label.configure(text=formatted_time)
        history_page.after(1000, update_date)

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.5, rely=0.5, anchor = "center")

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.5, rely=0.5, anchor = "center")
    update_date()
    
    title_label = ctk.CTkLabel(history_page, text="Book History", font=("Arial", 30, "bold"), text_color="#5088FC")
    title_label.place(relx=0.5, rely=0.15, anchor="center")
    
    frame_box = ctk.CTkFrame(history_page, width=1100, height=600, fg_color="white", corner_radius=15, border_width=5, border_color="#5088FC")
    frame_box.place(relx=0.5, rely=0.23, anchor="n")
    image_cache = {}
    def load_image(filename, size=(50, 50)):
        if filename in image_cache:
            return image_cache[filename]
    
        try:
            with open(filename, "rb") as file:
                image_bytes = file.read()
            pil_image = Image.open(io.BytesIO(image_bytes))
            ctk_image = ctk.CTkImage(pil_image, size=size)
            image_cache[filename] = ctk_image  # Cache the image
            return ctk_image
        except Exception as e:
           print(f"Error loading image {filename}: {e}")
           return None
    def configureBooks(nextNum, backButton, nextButton, nextX, nextY, backX, backY):
        global book_buttons, showBook
        if book_buttons:
            for button in book_buttons:
                button.destroy()
            book_buttons.clear()
        showBook = showBook + nextNum
        books = showBorrowHistory(RFID, 3, showBook)
        print(len(books))
        if books != []:
            nextbutton.place(relx=0.99, rely=0.1, anchor="e")
        else:
            nextbutton.place_forget()
        insert_book_buttons(books)
        if showBook >= 3:
            backbutton.place(relx=0.93, rely=0.1, anchor="e")
        else:
            backbutton.place_forget()

    backimage = load_image("back.png", size=(40, 40))
    backbutton = ctk.CTkButton(frame_box, image=backimage, text="", fg_color="white", hover_color="lightgray", width=30, height=70, command= lambda: configureBooks(-3, backbutton, backbutton, 0.93, 0.1, .99, 0.1))
    backbutton.image = backimage
    
    nextimage = load_image("next.png", size=(40, 40))
    nextbutton = ctk.CTkButton(frame_box, image=nextimage, text="", fg_color="white", hover_color="lightgray", width=30, height=70,  command= lambda: configureBooks(3, backbutton, nextbutton, 0.93, 0.1, .99, 0.1))
    nextbutton.place(relx=0.99, rely=0.1, anchor="e")
    nextbutton.image = nextimage
    
    def insert_book_buttons(books):
        print(enumerate(books))
        for i, (blob, title, author, borrowed, returned, bookID) in enumerate(books):
            try:
                image = Image.open(io.BytesIO(blob)).resize((100, 150))
                ctk_image = ctk.CTkImage(light_image=image, size=(100, 150))
            except Exception as e:
                print(f"Error loading image {i}: {e}")
                continue
        
            # Create book button
            print(bookID)
            book_button = ctk.CTkButton(history_page, text = "", image=ctk_image, compound="top", fg_color="white", hover_color="lightblue", text_color="black", font=("Arial", 14, "bold"), 
                                        command = lambda bookID=bookID: book_profile(content, bookID))
            book_button.place(relx=0.14, rely=0.38 + (i * 0.20), anchor="w")
            book_button.image = ctk_image  # Keep reference to prevent garbage collection
            book_buttons.append(book_button)
        
            # Create labels for title, author, borrowed, and returned dates
            titleText = ctk.CTkLabel(history_page, text=title, font=("Arial", 18, "bold"), fg_color="white", text_color="black", wraplength=350, justify="left")
            titleText.place(relx=0.28, rely=0.33 + (i * 0.20))

            authorText = ctk.CTkLabel(history_page, text=author, font=("Arial", 18), fg_color="white", text_color="black")
            authorText.place(relx=0.28, rely=0.38 + (i * 0.20))

            labelBorrowed = ctk.CTkLabel(history_page, text="Borrowed:", font=("Arial", 17, "bold"), text_color="red", fg_color="white")
            labelBorrowed.place(relx=0.60, rely=0.33 + (i * 0.20))

            date_borrowed = ctk.CTkLabel(history_page, text=borrowed, font=("Arial", 17), fg_color="white", text_color="black")
            date_borrowed.place(relx=0.66, rely=0.33 + (i * 0.20))

            labelReturned = ctk.CTkLabel(history_page, text="Returned:", font=("Arial", 17, "bold"), text_color="red", fg_color="white")
            labelReturned.place(relx=0.60, rely=0.36 + (i * 0.20))

            date_returned = ctk.CTkLabel(history_page, text=returned, font=("Arial", 17), fg_color="white", text_color="black")
            date_returned.place(relx=0.66, rely=0.36 + (i * 0.20))
            
            book_buttons.append(titleText)
            book_buttons.append(authorText)
            book_buttons.append(date_borrowed)
            book_buttons.append(date_returned)
            book_buttons.append(labelReturned)
            book_buttons.append(labelBorrowed)
    def load_book_history_async(RFID):
        def fetch_books():
            books = showBorrowHistory(RFID, 3, showBook)
            print(len(books)) # Fetch data in the background
            history_page.after(0, lambda: insert_book_buttons(books))  # Update UI on main thread

        thread = threading.Thread(target=fetch_books, daemon=True)
        thread.start()
 
# Call this function instead of directly fetching books
    load_book_history_async(RFID)
