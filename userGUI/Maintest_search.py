import customtkinter as ctk
import tkinter as tk
from PIL import Image
import io
from bnd import *
from Book_profile import *
from keyboard import *

def load_image(filename, size=(55, 55)):
    try:
        with open(filename, "rb") as file:
            image_bytes = file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        return ctk.CTkImage(pil_image, size=size)
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        return None
    
open("search_icon.png", "rb")
open("next.png", "rb")
open("back.png", "rb")

# global var

genres = ["General Knowledge", "Philosophy & Psychology", "Religion", "Social Sciences", "Languages", "Science", "Technology", "Arts & Recreation", "Literature", "History & Geography"]
firstSectionNum = 0
secondSectionNum = 0
book_buttons = []

def book_search(content, genresnum):

    global genres, book_buttons, firstSectionNum, secondSectionNum
    firstSectionNum = 0
    secondSectionNum = 0

    # Get the genre using the genresnum index
    genre = genres[genresnum]
    
    def booksOutput(genre, sectionName, num):
        global firstSectionNum, secondSectionNum

        # Determine the section to fetch from
        if sectionName == "firstSectionNum":
            sectionIndex = firstSectionNum
        elif sectionName == "secondSectionNum":
            sectionIndex = secondSectionNum + 3

        # Adjust sectionIndex and ensure it is not negative
        sectionIndex = sectionIndex - num

        # Fetch books using the adjusted sectionIndex
        books = showGenreBooks(genre, sectionIndex, sectionIndex + 3)

        # Increment the section number if books exist
        sectionIndex += 3
        if sectionName == "firstSectionNum":
            firstSectionNum = sectionIndex
        elif sectionName == "secondSectionNum":
            secondSectionNum = sectionIndex

        return books
    
    def firstSection(genre, num, sectionName, nextButton, prevButton):
        global firstSectionNum, secondSectionNum, book_buttons
        # Determine which section number to adjust
        if sectionName == "firstSectionNum":
            sectionVar = firstSectionNum
            rely_value = 0.33
        elif sectionName == "secondSectionNum":
            sectionVar = secondSectionNum
            rely_value = 0.76
            # Hide 'Prev' if at the first section
        if sectionVar - num <= 0:
            nextButton.place(relx=0.92, rely=0.09, anchor='center')
            prevButton.place_forget()
        else:
            print("pwede pa")
            prevButton.place(relx=0.86, rely=0.09, anchor='center')
        try:
            # Fetch books
            books = booksOutput(genre, sectionName, num)
            if sectionName == "firstSectionNum":
                showBooks(books, 0.33)
            elif sectionName == "secondSectionNum":
                showBooks(books, 0.75)
            if len(books) == 6:
                nextButton.place(relx=0.92, rely=0.09, anchor='center')
            else:
                nextButton.place_forget() # No more books, hide Next button
        except IndexError as err:
            print(err)
            
    search_image = load_image("search_icon.png", size=(50, 50))
    next_image = load_image("next.png", size=(40, 40))
    back_image = load_image("back.png", size=(40, 40))

    # Create search page frame
    search_border = ctk.CTkFrame(content, width=800, height=85, bg_color="white", fg_color='white', corner_radius=15)
    search_border.place(relx=0.5, rely=0.1, anchor='center')

    # Create the search bar entry inside the border
    search_bar = ctk.CTkEntry(search_border, width=750, height=70, corner_radius=30, bg_color='white', fg_color='white',
                              text_color="black", placeholder_text="Search bar", font=("Arial", 20))
    search_bar.place(relx=0.5, rely=0.5, anchor="center")
    search_bar.bind("<Button-1>", lambda event: open_keyboard(content, search_bar, event))

    search_button = ctk.CTkButton(search_bar, text='', image=search_image, width=75, fg_color='white',
                                  command=lambda: searchBooks("Title", search_bar.get(), 6, 0))
    search_button.place(relx=0.98, rely=0.5, anchor='e')

    # Frame for displaying books
    books = ctk.CTkFrame(content, width=1400, height=650, fg_color="white", bg_color="white",
                         corner_radius=20, border_width=15, border_color="White")
    books.place(relx=0.5, rely=0.55, anchor="center")

    genre_label = ctk.CTkLabel(books, text=genre, font=("Arial", 30, "bold"), text_color="Blue")
    genre_label.place(relx=0.06, rely=0.1, anchor="w")

    # Add divider lines
    divider1 = ctk.CTkFrame(books, width=1200, height=2, fg_color="grey")
    divider1.place(relx=0.5, rely=0.13, anchor="center")
    def buttonConfig(num):
        global book_buttons
        for button, y_val, title, unavailable in book_buttons:  # Iterate over a copy to avoid modification issues
            button.destroy()
            title.destroy()
            if unavailable:
                unavailable.destroy()
        firstSection(genre, num, "firstSectionNum", next_btn, prev_btn)
        firstSection(genre, (num + 3), "secondSectionNum", next_btn, prev_btn)
    next_btn = ctk.CTkButton(books, text="", image=next_image, bg_color="white",width=50, fg_color="white", 
                                command=lambda: buttonConfig(0))
    next_btn.place(relx=0.92, rely=0.09, anchor='center')

    prev_btn = ctk.CTkButton(books, text="", image=back_image, bg_color="white",width=50, fg_color="white", 
                                command = lambda: buttonConfig(6))

    def showBooks(bookArray, y):
        global book_buttons
        # Define positions for the buttons and labels
        positions = [(0.2, y), (0.5, y), (0.8, y)]  # Positions for books
        print(f"Button positions: {positions}")

        for i, (id, blob, title, availability) in enumerate(bookArray):
            try:
                # Load image from binary data
                image = Image.open(io.BytesIO(blob)).resize((136, 205))
                ctk_image = ctk.CTkImage(light_image=image, size=(136, 205))
            except Exception as e:
                print(f"Error loading image {i}: {e}")
                continue
            
            # Create book button
            book_button = ctk.CTkButton(
                books, image=ctk_image, compound="top", text= "",
                fg_color="white", hover_color="lightblue", command = lambda id=id: book_profile(content, id)
            )
            titleLabel = ctk.CTkLabel(books, text=title, font=("Poppins", 17, "bold"), text_color="black", wraplength=300)
            titleLabel.place(relx=positions[i][0], rely=(positions[i][1])+0.185, anchor="center")
            if availability == 0:
                unavailableBox = ctk.CTkFrame(books, width=150, height=20, fg_color="#8c1c2d", corner_radius= 50)
                unavailableBox.place(relx=positions[i][0], rely=(positions[i][1])+0.225, anchor="center")
                unavailableText = ctk.CTkLabel(unavailableBox, text="UNAVAILABLE", font=("Poppins", 12.5, "bold"), text_color="white", wraplength=300, height= 10)
                unavailableText.place(relx=0.5, rely=0.53, anchor="center")
            else:
                unavailableBox = None
            # Place button using predefined positions
            book_button.place(relx=positions[i][0], rely=(positions[i][1]), anchor="center")
            book_button.image = ctk_image  # Keep reference to prevent garbage collection
            book_buttons.append((book_button, y, titleLabel, unavailableBox))
            # Fetch books from two genres
    firstSection(genre, 0, "firstSectionNum", next_btn, prev_btn)
    firstSection(genre, 0, "secondSectionNum", next_btn, prev_btn)

    ### SA MAY LITERAL NA SEARCH NAMAN ############   

    def searchTitle(searchedItem, num):
        # intialize sets and arrays
        seen_ids = set() # tracking duplicates, based on sa Book ID
        combinedBookArray = [] # to combine results from title and author search
        for widget in books.winfo_children():
            widget.destroy()
    
    # Try to search by title first
        bookArray_Title = searchBooks("Title", searchedItem, 6, num)
    
    # Then search by author
        bookArray_Author = searchBooks("Author", searchedItem, 6, num)
    
    # for title results first
        for book in bookArray_Title:
            book_id = book[0]  # First element is the book ID, grab for checking duplicates
            if book_id not in seen_ids:
                # bnd showBooks function, grab ID, Blob, Title and Availability
                rearranged_book = (book[0], book[2], book[3], book[4])  # ID, Blob, Title, Availability
                combinedBookArray.append(rearranged_book)
                seen_ids.add(book_id) # add to list IDs seen
    
    # for author results
        for book in bookArray_Author:
            book_id = book[0]  
        if book_id not in seen_ids:
            rearranged_book = (book[0], book[2], book[3], book[4])  # ID, Blob, Title, Availability
            combinedBookArray.append(rearranged_book)
            seen_ids.add(book_id)
    
    # Para malaman if search worked or not (totes for design)
        search_header = ctk.CTkLabel(books, text=f"Search Results for: '{searchedItem}'", 
                              font=("Arial", 30, "bold"), text_color="Blue")
        search_header.place(relx=0.06, rely=0.1, anchor="w")
    
    # for debuggingggg
    
        print("length of the books Searched: ", len(combinedBookArray))
    
    # Show first 3 books
        if len(combinedBookArray) > 0:
            showBooks(combinedBookArray[0:3], 0.33)
    
    # Show next 3 books if available
        if len(combinedBookArray) > 3:
            print("extending")
            showBooks(combinedBookArray[3:6], 0.76)
    
        if len(combinedBookArray) > num + 6:
            search_next_button = ctk.CTkButton(books, text='', image=next_image, bg_color="white", width=50, fg_color="white", 
                                         command=lambda: searchTitle(searchedItem, (num + 6)))
            search_next_button.place(relx=0.92, rely=0.09, anchor='center')
    
        if num >= 6:
            search_back_button = ctk.CTkButton(books, text='', image=back_image, bg_color="white", width=50, fg_color="white", 
                                         command=lambda: searchTitle(searchedItem, (num - 6)))
            search_back_button.place(relx=0.86, rely=0.09, anchor='center')

    def enterSearch():
        close()
        input = search_bar.get()
        searchTitle(input, 0)

    search_button = ctk.CTkButton(search_bar, text='', image=search_image, width=75, fg_color='white', command=enterSearch)
    search_button.place(relx=0.98, rely=0.5, anchor='e')