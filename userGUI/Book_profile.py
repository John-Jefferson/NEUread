import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
from datetime import datetime
import pytz
from bnd import *
from io import BytesIO

def book_profile(content, bookID):
    for widget in content.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    print(bookID)
    ww = content.winfo_screenwidth()
    wh = content.winfo_screenheight()
    book = searchBookID(bookID)
    print(len(book[0]))
    image = Image.open(BytesIO(book[0][4]))  # Convert binary to image

# Apply add_corners function and set size
    book_cover_image = ctk.CTkImage(image, size=((0.16 * ww), (0.46 * wh)))

    profile = tk.Frame(content)
    profile.place(relx=0, rely=0, relwidth=1, relheight=1)

    time_border = ctk.CTkFrame(profile, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(profile, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05) 

    def update_date():
        ph_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.now(ph_timezone)
        formatted_date = current_time.strftime("%B %d, %Y")
        formatted_time = current_time.strftime("%I:%M %p")
        date_label.configure(text=formatted_date)
        time_label.configure(text=formatted_time)
        profile.after(1000, update_date)

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.5, rely=0.5, anchor = "center")

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.5, rely=0.5, anchor = "center")
    update_date()

    info = ctk.CTkFrame(profile, width=(0.78 * ww), height=(0.75 * wh), fg_color="white", 
                      corner_radius=20, border_width=5, border_color="#5088FC")
    info.place(relx=0.5, rely=0.55, anchor="center") 

    page_label = ctk.CTkLabel(info, text='Book Profile', font=("Arial", 40, "bold"), text_color="blue")
    page_label.place(relx=0.19, rely=0.075, anchor='center')

    book_cover = ctk.CTkLabel(info, text='', image=book_cover_image)
    book_cover.place(relx=0.0855, rely=0.12)
    bookState = []
    if book[0][3] != 0:
        bookState.append("AVAILABLE")
        bookState.append("green")
    else:
        bookState.append("UNAVAILABLE")
        bookState.append("red")
    availability_border = ctk.CTkFrame(info, width=(0.14 * ww), height=(0.06 * wh), fg_color=bookState[1], corner_radius=20, border_width=15, border_color=bookState[1])
    availability_border.place(relx=0.1, rely=0.8)
    availability = ctk.CTkLabel(availability_border, text=bookState[0], font=("Arial", 25, "bold"), text_color="white", bg_color=bookState[1])
    availability.place(relx=0.13, rely=0.2)

    book_title = ctk.CTkLabel(info, text=book[0][0], font=("Arial", 32, "bold"), text_color="black")
    book_title.place(relx=0.4, rely=0.1)

    book_author = ctk.CTkLabel(info, text=('Author: ' + book[0][1]), font=("Arial", 24), text_color="black")
    book_author.place(relx=0.4, rely=0.18)

    book_publish = ctk.CTkLabel(info, text=f"Year Published: {book[0][6]}", font=("Arial", 24, "bold"), text_color="blue")
    book_publish.place(relx=0.4, rely=0.22)

    book_genre  = ctk.CTkLabel(info, text=('Genre: ' + book[0][5]), font=("Arial", 24, "bold"), text_color="blue")
    book_genre.place(relx=0.4, rely=0.26)

    book_adress = ctk.CTkLabel(info, text=f'Shelf: {book[0][7]}', font=("Arial", 24, "bold"), text_color="blue")

    book_adress.place(relx=0.4, rely=0.3)
    book_description  = ctk.CTkLabel(info, text= book[0][2], 
                                     justify='left', font=("Times New Roman", 24), text_color="black", wraplength=500)
    book_description.place(relx=0.4, rely=0.36)