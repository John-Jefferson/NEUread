import customtkinter as ctk
import tkinter as tk
from PIL import Image
import io
import pytz
from datetime import datetime
from Maintest_search import book_search
from keyboard import *

# Function to load and resize images
def load_image(path, size=(170, 250)):
    image = Image.open(path).resize(size)
    return ctk.CTkImage(light_image=image, size=size)

# Load Images
search_image = load_image("search_icon.png", size=(50, 50))
general_knowledge = load_image("gk.png")
philosophy = load_image("phil.png")
religion = load_image("rel.png")
social_sciences = load_image("soc.png")
language = load_image("lng.png")
science = load_image("sci.png")
technology = load_image("tech.png")
arts = load_image("art.png")
literature = load_image("lit.png")
history = load_image("his.png")

def genre_pick(content, root):

    genres_page = tk.Frame(content)
    genres_page.place(relx=0, rely=0, relwidth=1, relheight=1)

    ww = genres_page.winfo_screenwidth()
    wh = genres_page.winfo_screenheight()
    time_border = ctk.CTkFrame(genres_page, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(genres_page, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05)

    def update_date():
        ph_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.now(ph_timezone)
        formatted_date = current_time.strftime("%B %d, %Y")
        formatted_time = current_time.strftime("%I:%M %p")
        date_label.configure(text=formatted_date)
        time_label.configure(text=formatted_time)
        genres_page.after(1000, update_date)

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.07, rely=0.2)

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.07, rely=0.2)
    update_date()

    search_border = ctk.CTkFrame(genres_page, width=800, height=85,bg_color="#f2f3f7", fg_color='white', corner_radius=15)
    search_border.place(relx=0.5, rely=0.1, anchor='center')

    search_bar = ctk.CTkEntry(search_border, width=750, height=70, corner_radius=30, bg_color='white', fg_color='white',
                              text_color="black", placeholder_text="Search bar", font=("Arial", 20))
    search_bar.place(relx=0.5, rely=0.5, anchor="center")
    search_bar.bind("<Button-1>", lambda event: open_keyboard(root, search_bar, event))

    search_button = ctk.CTkButton(search_bar, text='', image=search_image, width=75, fg_color='white')
    search_button.place(relx=0.98, rely=0.5, anchor='e')

    genres = ctk.CTkFrame(genres_page, width=1400, height=650, fg_color="white", corner_radius=20, border_width=15, border_color="white")
    genres.place(relx=0.5, rely=0.55, anchor="center")

    # Genre Buttons
    gk_button = ctk.CTkButton(genres, image=general_knowledge, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 0))
    gk_button.place(relx=0.05, rely=0.05)
    
    phil_button = ctk.CTkButton(genres, image=philosophy, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 1))
    phil_button.place(relx=0.25, rely=0.05)

    religion_button = ctk.CTkButton(genres, image=religion, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 2))
    religion_button.place(relx=0.45, rely=0.05)

    socsci_button = ctk.CTkButton(genres, image=social_sciences, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 3))
    socsci_button.place(relx=0.65, rely=0.05)
    
    language_button = ctk.CTkButton(genres, image=language, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 4))
    language_button.place(relx=0.85, rely=0.05)

    science_button = ctk.CTkButton(genres, image=science, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 5))
    science_button.place(relx=0.05, rely=0.5)

    technology_button = ctk.CTkButton(genres, image=technology, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 6))
    technology_button.place(relx=0.25, rely=0.5)

    arts_button = ctk.CTkButton(genres, image=arts, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 7))
    arts_button.place(relx=0.45, rely=0.5)

    literature_button = ctk.CTkButton(genres, image=literature, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 8))
    literature_button.place(relx=0.65, rely=0.5)

    history_button = ctk.CTkButton(genres, image=history, text="", fg_color="white", hover_color="#e0e0e0", command=lambda: book_search(content, 9))
    history_button.place(relx=0.85, rely=0.5)
