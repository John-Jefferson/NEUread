import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk  # Import Pillow for image resizing
import bcrypt
from tkinter import Canvas
from bnd import *
from datetime import datetime
from keyboard import *
from tkinter import filedialog, messagebox
import tkinter.messagebox as messagebox
import customtkinter as ctk
from tkinter import filedialog
popup_window_delete = None
popup_window_create = None
def errorNotif(err, content, root):
    notif_frame = ctk.CTkFrame(content, width=520, height=50, corner_radius=20, fg_color="#e61e1e", border_width=3, border_color="red")
    notif_frame.place(relx= 0.5, rely=0.85, anchor= "center")
    notif = ctk.CTkLabel(notif_frame, text=err, font=("Arial", 25, "bold"), text_color="dark red")
    notif.place(relx= 0.5, rely=0.5, anchor= "center")  # Show the label
    root.after(3000, lambda: notif_frame.destroy())
def successNotif(success, content, root):
    print("NAG START NA")
    notif_frame = ctk.CTkFrame(content, width=520, height=100, corner_radius=20, fg_color="#5ee332", border_width=3, border_color="#5088FC")
    notif_frame.place(relx= 0.5, rely=0.85, anchor= "center")
    notifTag = ctk.CTkLabel(notif_frame, text="Email Sending:", font=("Arial", 25, "bold"), text_color="#5088FC")
    notifTag.place(relx= 0.5, rely=0.3, anchor= "center")
    notif = ctk.CTkLabel(notif_frame, text=success, font=("Arial", 25, "bold"), text_color="#5088FC")
    notif.place(relx= 0.5, rely=0.7, anchor= "center")  # Show the label
    root.after(3000, lambda: notif_frame.destroy())
    
def admin(content, return_to_idle, root):
    passwd = "$2b$12$NhmTJ0kKyQdVdRJoIGbHBOA5kb1Bb7EB5sXY2MIprdTC5zC3Aqa2q"
    ww = content.winfo_screenwidth()
    wh = content.winfo_screenheight()
    for widget in content.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    # Load and resize background image dynamically
    original_bg = Image.open("Admin_Interface_Design.png")# Load image
    resized_bg = original_bg.resize((ww, wh))  # Resize to screen size (ANTIALIAS is no longer needed)
    bg_image = ImageTk.PhotoImage(resized_bg)  # Convert for Tkinter

    # Set background image properly
    bg = tk.Label(content,image=bg_image)
    bg.place(relx=0, rely=0, relwidth=1, relheight=1)
    content.bg_image = bg_image

    password_frame = ctk.CTkFrame(content, width=1350, height=700, fg_color="white", border_color="grey")
    password_frame.place(relx=0.5, rely=0.5, anchor= "center")

    enter_password = ctk.CTkLabel(password_frame, text="Enter The Password\nTo Proceed", 
                                  font=("Arial", 75, 'bold'), text_color="Black")
    enter_password.place(relx=0.5, rely=0.3, anchor="center")

    password = ctk.CTkEntry(password_frame, width=650, height=65, font=("Arial", 32, 'bold'), 
                            fg_color="#89AEFD", text_color="Black", corner_radius=50, border_width=0, show="•")
    password.bind("<Button-1>", lambda event: open_keyboard(root, password, event))
    password.place(relx=0.26, rely=0.5)
    def submit_password():
        close()
        user_input = password.get()
        access = bcrypt.checkpw(user_input.encode(), passwd.encode())
        if access:
            adminMain(root, return_to_idle, content)
        else:
            errorNotif("Wrong Admin Password", content, root)
    enter_option = ctk.CTkButton(password_frame, text="Enter", width=200, height=60, corner_radius=50, 
                                 bg_color="white", fg_color="#5088FC", font=("Arial", 32, 'bold'), text_color="White", command=submit_password)
    enter_option.place(relx=0.35, rely=0.67)

    cancel_option = ctk.CTkButton(password_frame, text="Cancel", width=200, height=60, corner_radius=50, 
                                  bg_color="white", border_width=5, border_color='#89AEFD', fg_color="white", 
                                  font=("Arial", 24, 'bold'), text_color="#5088FC", command= return_to_idle)
    cancel_option.place(relx=0.51, rely=0.67)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, color="white"):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, fill=color, outline=color)
def completeTransaction(root, on_frame_touch, emailAddress, datefrom, dateTo):
    send_email_with_attachment(emailAddress, datefrom, dateTo)
    Data_Send_page = tk.Frame(root, width=500, height=300, bg="89AEFD")
    Data_Send_page.pack(fill="both", expand=True)
    Data_Send_label = tk.Label(Data_Send_page, text='The data has been successfully emailed to CSD.' , fg="white", font=("Arial", 60, "bold"), 
                        bg="89AEFD", wraplength=1000)
    Data_Send_label.place(relx=0.5, rely=0.5, anchor="center")
    pop_up_label2 = tk.Label(Data_Send_page, text="Please touch the screen to continue", fg="white", 
                             font=("Arial", 20, "bold"), bg="89AEFD")
    pop_up_label2.place(relx=0.5, rely=0.80, anchor="center")
    Data_Send_label.bind("<Button-1>", lambda event: on_frame_touch(event, Data_Send_label))
def adminMain(root, return_to_idle, content):
    innitNums = getUserAndBookNum()
    ww = root.winfo_screenwidth()
    wh = root.winfo_screenheight()
    datefrom = None
    dateTo = None
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.place(x=0, y=0)

#(Left, Top, Right, Bottom)
    create_rounded_rectangle(canvas, 80, 220, 80 + 725, 200 + 290, radius=50, color="#89AEFD")  # Borrowed Books Box
    create_rounded_rectangle(canvas, 550, 240, 550 + 225, 230 + 235, radius=50, color="#5088FC")  # Returned Books Box
    create_rounded_rectangle(canvas, 833, 220, 720 + 400, 200 + 290, radius=50, color="#5088FC")  # User Registered Box
    create_rounded_rectangle(canvas, 80, 515, 80 + 250, 400 + 350, radius=50, color="#5088FC")  # Books in System Box
    create_rounded_rectangle(canvas, 360, 515, 350 + 453, 525 + 220, radius=50, color="#89AEFD") # Users With Penalty Box
    create_rounded_rectangle(canvas, 1150, 220, 720 + 765, 200 + 443, radius=50, color="#89AEFD") # Data Shown Box

    logo = ctk.CTkImage(
    Image.open("logoo.png"),
    size=(int(0.26 * ww), int(0.23 * wh))
)
    book = ctk.CTkImage(
    Image.open("books.png"),
    size=(int(0.20 * ww), int(0.30 * wh))
)
    bookopen = ctk.CTkImage(
    Image.open("bookopen.png"),
    size=(int(0.16 * ww), int(0.2 * wh))
)

    person = ctk.CTkImage(
    Image.open("person.png"),
    size=(int(0.155 * ww), int(0.2 * wh))
)

    title_label = tk.Label(root, text="Hello, Admin!", font=("Arial", 47, "bold"), fg="#89AEFD")
    title_label.place(x=85, y=75)

    logo_label = ctk.CTkLabel(root, image=logo, text="")
    logo_label.place(x=1040, y=13)

# For borrowed books box
    bookopen_frame = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#89AEFD")
    bookopen_frame.place(x=120, y=275)
    bookopen_label = ctk.CTkLabel(bookopen_frame, image=bookopen, text="")
    bookopen_label.pack()
    bookopen = tk.Label(root, text="BORROWED BOOKS", font=("Arial", 17, "bold"), wraplength=200, fg="white", bg="#89AEFD")
    bookopen.place(x=375, y=270)

    bookopen_no = tk.Label(root, text="", font=("Arial", 38, "bold"), fg="white", bg="#89AEFD")
    bookopen_no.place(x=411, y=350)

# For returned books box
    returned_label= ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#5088FC")
    returned_label = tk.Label(root, text="RETURNED BOOKS", wraplength="200", font=("Arial", 17, "bold"), fg="white", bg="#5088FC")
    returned_label.place (x=598, y=270)

    returned_no = tk.Label(root, text="", font=("Arial", 38, "bold"), fg="white", bg="#5088FC")
    returned_no.place(x=644, y=350)

# For user registered box
    registered_label = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#5088FC")
    registered_label = tk.Label(root, text="USER REGISTERED", wraplength="200", font=("Arial", 17, "bold"), fg="white", bg="#5088FC")
    registered_label.place (x=900, y=265)

    registered_no = tk.Label(root, text=innitNums[0], font=("Arial", 38, "bold"), fg="white", bg="#5088FC")
    registered_no.place(x=950, y=350)

# For books in the system box
    bsystem_label = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#5088FC")
    bsystem_label = tk.Label(root, text="BOOKS IN THE SYSTEM", wraplength="200", font=("Arial", 17, "bold"), fg="white", bg="#5088FC")
    bsystem_label.place (x=120, y=550)
    #BORROW SECTION
    bsystem_no = tk.Label(root, text=innitNums[1], font=("Arial", 38, "bold"), fg="white", bg="#5088FC")
    bsystem_no.place(x=173, y=630)

# For user with penalty box
    person_frame = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#89AEFD")
    person_frame.place(x=550, y=550)
    person_label = tk.Label(root, text="USERS WITH", wraplength="200", font=("Arial", 17, "bold"), fg="white", bg="#89AEFD")
    person_label.place (x=395, y=550)
    person_label = tk.Label(root, text="PENALTY", wraplength="200", font=("Arial", 17, "bold"), fg="red", bg="#89AEFD")
    person_label.place (x=395, y=575)
    person_label = ctk.CTkLabel(person_frame, image=person, text="")
    person_label.pack()

    bsystem_no = tk.Label(root, text=innitNums[2], font=("Arial", 38, "bold"), fg="white", bg="#89AEFD")
    bsystem_no.place(x=430, y=630)

# For 3 books design
    book_label = ctk.CTkLabel(root, image=book, text="")
    book_label.place(x=810, y=500)

# For data shown box
    data_label = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="#5088FC")
    data_label = tk.Label(root, text="DATA FROM", wraplength="150", font=("Arial", 23, "bold"), fg="white", bg="#89AEFD")
    data_label.place (x=1310, y=290, anchor="center")

    date1_bar = ctk.CTkEntry(root, width=220, height=70, corner_radius=0, fg_color='white',
                              text_color="dark gray", placeholder_text="YYYY-MM-DD", font=("Arial", 23))
    date1_bar.bind("<Button-1>", lambda event: open_keyboard(root, date1_bar, event))
    date1_bar.place(x=1210, y=350)

    to_label = tk.Label(root, text="TO", wraplength="200", font=("Arial", 26, "bold"), fg="white", bg="#89AEFD")
    to_label.place (x=1320, y=445, anchor="center")

    date2_bar = ctk.CTkEntry(root, width=220, height=70, corner_radius=0, fg_color='white',
                              text_color="dark gray", placeholder_text="YYYY-MM-DD", font=("Arial", 23))
    date2_bar.bind("<Button-1>", lambda event: open_keyboard(root, date2_bar, event))
    date2_bar.place(x=1320, y=510, anchor="center")
    def showData():
        global datefrom, dateTo
        try:
            close()
            datetime.strptime(date1_bar.get(), "%Y-%m-%d")
            datetime.strptime(date2_bar.get(), "%Y-%m-%d")
            datefrom = date1_bar.get()
            dateTo = date2_bar.get()
        except ValueError:
            notif_frame = ctk.CTkFrame(root, width=400, height=30, corner_radius=20, fg_color="light blue", border_width=3, border_color="#89AEFD")
            notif_frame.place(x=1320, y=650, anchor="center")  # Position the frame
    
    # Add the text label inside the frame
            notif_label = ctk.CTkLabel(notif_frame, text="Error: Date format should be YYYY-MM-DD", font=("Arial", 20), text_color="black", fg_color="light blue")
            notif_label.place(relx=0.5, rely=0.5, anchor="center")  # Center text inside frame
            root.after(3000, lambda: notif_frame.place_forget())
            return
        borrow_count, return_count = BnRcount_rows(datefrom, dateTo)
        bookopen_no.config(text=borrow_count)
        returned_no.config(text=return_count)
    show_button = ctk.CTkButton(canvas, text="SHOW", width=280, height=40, corner_radius=50, 
                                   bg_color="#89AEFD", fg_color="#5088FC", font=("Arial", 24, 'bold'), text_color="White", command = showData)
    show_button.place(x=1320, y=590, anchor="center")  

# For under the export button
    csd_label = ctk.CTkFrame(root, width=int(0.02 * ww), height=int(0.01 * wh), fg_color="white")
    csd_label = ctk.CTkLabel (root, text='*Data must be sent to CSD', font = ("Arial", 15, 'bold'), text_color="Grey")
    csd_label.place (x=ww - 305, y=wh - 90)
    def on_frame_touch(event, frame):
        if event.widget == frame:
            frame.unbind("<Button-1>")
            admin(content, return_to_idle, root)
    def exportData(export_button):
        global datefrom, dateTo
        print("button Interactive")
        if datefrom == None or dateTo == None:
            return
        if not is_connected():
            errorNotif("Unable to send; No Internet", content, root)
            return
        export_button.configure(state="disabled")
        successNotif("Please wait as it process the email", content, root)
        root.after(100, lambda: completeTransaction(root, on_frame_touch, "yourFranzkafka@gmail.com", datefrom, dateTo))


# Pre-filled entry beside Export button
    email_entry = ctk.CTkEntry(canvas, width=300, height=60, corner_radius=50, 
                           fg_color='white', text_color="black", 
                           font=("Arial", 20), placeholder_text="Enter email")
    email_entry.insert(0, "csd@gmail.com")  # Insert default value
    email_entry.place(x=1320, y=wh - 205, anchor = "center")      # Adjust X so it's beside the button

# Export button
    export_button = ctk.CTkButton(canvas, text="Export", width=331, height=60, corner_radius=50, fg_color="#5088FC", font=("Arial", 24, 'bold'), 
                              text_color="White", command=lambda: exportData(export_button))
    export_button.place(x=1320, y=wh - 130, anchor = "center")

    button_img = ctk.CTkImage(
    Image.open("logOut.PNG"),
    size=(75, 75)
)
    button = ctk.CTkButton(root, image=button_img, text="", fg_color="transparent", hover_color="lightgray", border_width=0, corner_radius=1000, command = return_to_idle)

    button.place(x=40, y=780)
    import_button = ctk.CTkButton(root, text="Add Items", command=open_book_form, width=180, height=60, fg_color="#5088FC", text_color="white", font=("Arial", 16, "bold"), corner_radius= 50) 
    import_button.place(x=225, y=800)
    deleteBookButton = ctk.CTkButton(root, text="Delete Items", command=open_delete_book_form, width=180, height=60, fg_color="#5088FC", text_color="white", font=("Arial", 16, "bold"), corner_radius= 50) 
    deleteBookButton.place(x=500, y=800)
def open_book_form():
    global popup_window_create

    # If already open, focus and return
    if popup_window_create is not None and popup_window_create.winfo_exists():
        return
    form = tk.Toplevel()
    popup_window_create = form
    form.geometry("720x450")
    form.title("Add Book Entry")
    form.lift()  # Bring the form to the front
    form.attributes('-topmost', 1)

    entries = {}
    fields = [
        ("Book_ID", int), ("Title", str), ("Author", str), ("Description", str),
        ("Availability", int), ("Genre", str), ("Year_Publication", int), ("Book_Address", str)
    ]

    for i, (field, _) in enumerate(fields):
        label = ctk.CTkLabel(form, text=field, text_color="#5088FC", font=("Arial", 16, "bold"))
        label.grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = ctk.CTkEntry(form, width=400, border_color="#89AEFD", fg_color="#5088FC")
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

    # File selector for image
    def choose_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        image_path_var.set(file_path)

    image_path_var = ctk.StringVar()
    ctk.CTkLabel(form, text="Book_Cover", text_color="#5088FC", font=("Arial", 16, "bold")).grid(row=len(fields), column=0, padx=10, pady=5, sticky='e')
    ctk.CTkEntry(form, textvariable=image_path_var, width=300, state="readonly", border_color="#89AEFD", fg_color="#5088FC").grid(row=len(fields), column=1, padx=10, pady=5, sticky='w')
    ctk.CTkButton(form, text="Browse", command=choose_image, fg_color="#5088FC", hover_color="#1565C0", text_color="white", font=("Arial", 16, "bold")).grid(row=len(fields), column=2, padx=5)

    # Submit button
    def submit():
        # Validate that all fields are filled and the image is selected
        for field in fields:
            field_name = field[0]
            if not entries[field_name].get():
                messagebox.showerror("Input Error", f"The {field_name} field is required!")
                return
        
        if not image_path_var.get():
            messagebox.showerror("Input Error", "Book cover image is required!")
            return

        # Proceed with submitting the form
        data = {field[0]: field[1](entries[field[0]].get()) for field in fields}
        data['Book_Cover'] = image_path_var.get()

        try:
            insert_book(data)  # Assuming insert_book is defined elsewhere
            messagebox.showinfo("Success", "Book added successfully!")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding the book: {str(e)}")

    submit_btn = ctk.CTkButton(form, text="Submit", command=submit, fg_color="#5088FC", hover_color="#1565C0", text_color="white", font=("Arial", 16, "bold"))
    submit_btn.grid(row=len(fields)+1, column=1, pady=20)
    def on_close():
        global popup_window_delete
        popup_window_delete = None

    popup_window_delete.protocol("WM_DELETE_WINDOW", on_close)
    form.mainloop()
def open_delete_book_form():
    global popup_window_delete

    if popup_window_delete and popup_window_delete.winfo_exists():
        popup_window_delete.lift()
        popup_window_delete.focus()
        return

    popup_window_delete = tk.Toplevel()
    popup_window_delete.geometry("1200x500")
    popup_window_delete.title("Delete Book")
    popup_window_delete.attributes('-topmost', True)

    # Search Entry
    ctk.CTkLabel(popup_window_delete, text="Enter Book ID to search:", font=("Arial", 18, "bold"), text_color="#5088FC").pack(pady=10)
    book_id_entry = ctk.CTkEntry(popup_window_delete, width=400, height=40, fg_color="white", text_color="black", border_color="#5088FC", font=("Arial", 16))
    book_id_entry.pack()

    # Display Frame
    display_frame = ctk.CTkFrame(popup_window_delete, fg_color="#89AEFD", corner_radius=10)
    display_frame.pack(pady=20, padx=20, fill='both', expand=True)

    # Labels to show book data
    labels = {}
    for field in ["Book_ID", "Title", "Author", "Description", "Availability", "Genre", "Year_Publication", "Book_Address"]:
        lbl = ctk.CTkLabel(display_frame, text=f"{field}: ", font=("Arial", 25, "bold"), text_color="white", anchor='w')
        lbl.pack(fill='x', padx=10, pady=2)
        labels[field] = lbl

    # Delete button
    def delete_book():
        try:
            book_id = int(book_id_entry.get())
            delete_book_by_ID(book_id)
            messagebox.showinfo("Deleted", f"Book ID {book_id} has been deleted.")
            for lbl in labels.values():
                lbl.configure(text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {e}")
    def search_book():
        book_id = book_id_entry.get()
        if not book_id.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid numeric Book ID.")
            return

        data = searchBookIDtoDelete(book_id)
        print(data)
        if data:
            delete_btn.configure(state="normal")
            labels["Book_ID"].configure(text=f"Book_ID: {book_id}")
            labels["Title"].configure(text=f"Title: {data['Title']}")
            labels["Author"].configure(text=f"Author: {data['Author']}")
            labels["Description"].configure(text=f"Description: {data['Description']}")
            labels["Availability"].configure(text=f"Availability: {data['Availability']}")
            labels["Genre"].configure(text=f"Genre: {data['Genre']}")
            labels["Year_Publication"].configure(text=f"Year: {data['Year_Publication']}")
            labels["Book_Address"].configure(text=f"Address: {data['Book_Address']}")
        else:
            messagebox.showinfo("Not Found", "No book found with that ID.")
            delete_btn.configure(state="disabled")
            for lbl in labels.values():
                lbl.configure(text="")
    ctk.CTkButton(popup_window_delete, text="Search", command=search_book, fg_color="#5088FC", text_color="white", font=("Arial", 20, "bold")).pack(pady=10)
    delete_btn = ctk.CTkButton(popup_window_delete, text="Delete Book", command=delete_book, fg_color="#FF5A5F", text_color="white", state="disabled", font=("Arial", 20, "bold"))
    delete_btn.pack(pady=10)