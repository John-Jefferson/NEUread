import tkinter as tk
import customtkinter as ctk
from bnd import *
from datetime import datetime, timedelta
import time
from PIL import Image, ImageTk
import pytz
from keyboard import *
ww = None
wh = None
rfid_data = ""
adminRFID = False
bookRFID = False
userRFID = None
initialUser = None
bookID = None
Title = None
last_scan_time = 0
purpose = None
topLabel = None
bottomLabel = None

bookIcon = None
adminIcon = None
userIcon = None

bookPart = None
adminPart = None
userPart = None
inst_label = None
def Main_borrow_return_page(content, userID, main):
    global initialUser, purpose, ww, wh, rfid_data, adminRFID, bookRFID, userRFID, bookID, Title, last_scan_time
    global topLabel, bottomLabel, bookIcon, adminIcon, userIcon, bookPart, adminPart, userPart, inst_label
    
    ww = content.winfo_screenwidth()
    wh = content.winfo_screenheight()
    initialUser = userID
    purpose = None
    rfid_data = ""
    adminRFID = False
    bookRFID = False
    userRFID = None
    bookID = None
    Title = None
    last_scan_time = 0
    topLabel = None
    bottomLabel = None
    inst_label = None

    bookIcon = None
    adminIcon = None
    userIcon = None
    
    bookPart = None
    adminPart = None
    userPart = None
    for widget in content.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    frame = tk.Frame(content, bg='#f2f3f7')
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    time_border = ctk.CTkFrame(frame, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(frame, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05)

    def update_date():
        ph_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.now(ph_timezone)
        formatted_date = current_time.strftime("%B %d, %Y")
        formatted_time = current_time.strftime("%I:%M %p")
        date_label.configure(text=formatted_date)
        time_label.configure(text=formatted_time)
        frame.after(1000, update_date)

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.5, rely=0.5, anchor = "center")

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.5, rely=0.5, anchor = "center")
    update_date()
    
# Load Button Icons
    borrow_icon = ctk.CTkImage(light_image=Image.open("borrowbtn.png").resize((280, 260)),
                           dark_image=Image.open("borrowbtn.png").resize((280, 260)),
                           size=(280, 260))

    return_icon = ctk.CTkImage(light_image=Image.open("returnbtn.png").resize((280, 260)),
                           dark_image=Image.open("returnbtn.png").resize((280, 260)),
                           size=(280, 260))

# Borrow Button
    borrow_btn = ctk.CTkButton(frame, text="Borrow", font=('Arial', 20, "bold"), width=400, height=600,
                           fg_color="white", text_color="black",
                           image=borrow_icon, compound="top", corner_radius=10,
                           command=lambda: borrow_page(content, main, "Borrow"))
    borrow_btn.place(relx=0.3, rely=0.5, anchor="center")  # Adjust placement

# Return Button
    return_btn = ctk.CTkButton(frame, text="Return", font=('Arial', 20, "bold"), width=400, height=600,
                           fg_color="white", text_color="black",
                           image=return_icon, compound="top", corner_radius=10,
                           command=lambda: borrow_page(content, main, "Return"))
    return_btn.place(relx=0.7, rely=0.5, anchor="center")  # Adjust placement
search = open("next_blue.png", "rb")
dot = open("dot_pic.png", "rb")
admin_profile = open("admin_pic.png", "rb")

book = open("book_pic.png", "rb")
ON_admin_profile = open("admin_blue_pic.png", "rb")

DONE_book = open("book_done_pic.png", "rb")
DONE_admin = open("admin_done_prev_ui.png", "rb")

user_profile = open("userGray.png", "rb")
ON_user_profile = open("userBlue.png", "rb")

# place here for all photo images
def borrow_page(content, root, pressedPurpose):
    global purpose, topLabel,bottomLabel, bookIcon, adminIcon, userIcon, ww, wh, bookPart, adminPart, userPart, inst_label
    purpose = pressedPurpose
    bors = tk.Frame(content)
    bors.place(relx=0, rely=0, relwidth=1, relheight=1)
    search_image = ctk.CTkImage(Image.open(search), size=((0.033 * ww), (0.06 * wh))) 
    book_pic = ctk.CTkImage(Image.open(book), size=((0.2 * ww), (0.35 * wh))) 
    dot_pic = ctk.CTkImage(Image.open(dot), size=((0.065 * ww), (0.06 * wh)))
    user_pic = ctk.CTkImage(Image.open(admin_profile), size=((0.13 * ww), (0.23 * wh))) 
    admin_pic = ctk.CTkImage(Image.open(user_profile), size=((0.13 * ww), (0.23 * wh))) 

    bookIcon = book_pic
    adminIcon = admin_pic
    userIcon = user_pic

    time_border = ctk.CTkFrame(bors, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(bors, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05)

    def update_date():
        ph_timezone = pytz.timezone("Asia/Manila")
        current_time = datetime.now(ph_timezone)
        formatted_date = current_time.strftime("%B %d, %Y")
        formatted_time = current_time.strftime("%I:%M %p")
        date_label.configure(text=formatted_date)
        time_label.configure(text=formatted_time)
        bors.after(1000, update_date)

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.5, rely=0.5, anchor = "center")

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.5, rely=0.5, anchor = "center")
    update_date()

    page_bg = ctk.CTkFrame(bors, width=(0.510 * ww), height=(0.14 * wh), fg_color="white", 
                      corner_radius=20)
    page_bg.place(relx=0.5, rely=0.20, anchor='center')

    page_label = ctk.CTkLabel(page_bg, text=f'{purpose} Book', font=("Arial", 30, "bold"), text_color="blue",  wraplength= 700)
    page_label.place(relx=0.5, rely=0.5, anchor= "center")
    topLabel = page_label

    book_label = ctk.CTkLabel(bors, text='', image=book_pic, width=(0.05 * ww))
    book_label.place(relx=0.20, rely=0.5, anchor="center")

    dot1_label = ctk.CTkLabel(bors, text='', image=dot_pic, width=(0.05 * ww))
    dot1_label.place(relx=0.35, rely=0.5, anchor="center")

    user = ctk.CTkLabel(bors, text='', image=user_pic, width=(0.05 * ww))
    user.place(relx=0.5, rely=0.5, anchor="center")

    dot2_label = ctk.CTkLabel(bors, text='', image=dot_pic, width=(0.05 * ww))
    dot2_label.place(relx=0.645, rely=0.5, anchor="center")

    admin = ctk.CTkLabel(bors, text='', image=admin_pic, width=(0.05 * ww))
    admin.place(relx=0.80, rely=0.5, anchor="center")

    inst_label = ctk.CTkLabel(bors, text='Check the spine of the book for Book ID (Example: 1027)', 
                           font=("Arial", 20), text_color="Black")
    inst_label.place(relx=0.5, rely=0.75, anchor="center")

    root.bind("<Key>", lambda event: keyPressed(event, content, root)) #ENTER RFID NA

    cancel_button = ctk.CTkButton(bors, text='CANCEL', height=50, width=(0.05 * ww), fg_color='blue', font=("Arial", 25, "bold"), command = lambda: Main_borrow_return_page(content, userRFID, root), 
                                  text_color="White", corner_radius=20)
    cancel_button.place(relx=0.45, rely=0.90)

    ask_label = ctk.CTkLabel(bors, text="Please ask a librarian to tap the security card.", font=("Arial", 30), text_color="Black")
    bottomLabel = ask_label

    bookPart = book_label
    adminPart = user
    userPart = admin

def errorNotif(err, content, root):
    notif_frame = ctk.CTkFrame(content, width=520, height=50, corner_radius=20, fg_color="#e61e1e", border_width=3, border_color="red")
    notif_frame.place(relx= 0.5, rely=0.7, anchor= "center")
    notif = ctk.CTkLabel(notif_frame, text=err, font=("Arial", 25, "bold"), text_color="dark red")
    notif.place(relx= 0.5, rely=0.5, anchor= "center")  # Show the label
    root.after(3000, lambda: notif_frame.destroy())
def successNotif(success, content, root):
    print("NAG START NA")
    notif_frame = ctk.CTkFrame(content, width=520, height=100, corner_radius=20, fg_color="#5ee332", border_width=3, border_color="green")
    notif_frame.place(relx= 0.5, rely=0.7, anchor= "center")
    notifTag = ctk.CTkLabel(notif_frame, text="Transaction Successful:", font=("Arial", 25, "bold"), text_color="green")
    notifTag.place(relx= 0.5, rely=0.3, anchor= "center")
    notif = ctk.CTkLabel(notif_frame, text=success, font=("Arial", 25, "bold"), text_color="green")
    notif.place(relx= 0.5, rely=0.7, anchor= "center")  # Show the label
    root.after(3000, lambda: notif_frame.destroy())

def save_input(book_id, inst_label, content, root):
    global bookID, Title, ww, wh, initialUser, rfid_data
    penalty = checkPenalty(initialUser)
    if penalty:
        errorNotif("You have Penalty", content, root)
        rfid_data = ""
        return
    search_result = searchBookID(book_id)
    if not search_result:
        errorNotif("Book ID doesnt exist", content, root)
        rfid_data = ""
        return
    if purpose == "Borrow" and search_result[0][3] != 1:
        errorNotif("Book is currently unavailable", content, root)
        rfid_data = ""
        return
    exceeds = ifTheyExceedBorrow(initialUser)
    if purpose == "Borrow" and exceeds:
        errorNotif("exceeded the limit of borrowing", content, root)
        rfid_data = ""
        return
    hasTheBook = ifTheyHaveTheBook(book_id, initialUser)
    if purpose == "Return" and not hasTheBook:
        errorNotif("You're not the one who borrowed the book", content, root)
        rfid_data = ""
        return
    if (search_result[0][3] != 0 and purpose == "Return"):
        errorNotif("Book is already available", content, root)
        rfid_data = ""
        return
    
    print(f"Book ID Entered: {search_result[0][0]}", ", kukuhain na admin")
    inst_label.place_forget()
    bookID = book_id
    Title = search_result[0][0]
    close()
    getAdmin(content, root, search_result[0][0])
    rfid_data = ""

def getAdmin(content, root, Title):
    global topLabel, bookIcon, adminIcon, ww, wh, bookPart, adminPart, bottomLabel, purpose
    new_bookImage = ctk.CTkImage(
        light_image=Image.open(DONE_book),
        size=((0.13 * ww), (0.23 * wh))
    )
    new_adminImage = ctk.CTkImage(
        light_image=Image.open(ON_admin_profile),
        size=((0.2 * ww), (0.35 * wh))
    )

    bookPart.configure(image = new_bookImage)
    adminPart.configure(image = new_adminImage)
    topLabel.configure(text=f"You are {purpose}:\n '{Title}'")
    bottomLabel.place (relx=0.5, rely=0.81, anchor='n')

    root.bind("<Key>", lambda event: keyPressed(event, content, root))

def getUser():
    global topLabel, userIcon, adminIcon, ww, wh, adminPart, userPart, bottomLabel, DONE_admin, ON_user_profile

    new_adminImage = ctk.CTkImage(
        light_image=Image.open(DONE_admin),
        size=((0.13 * ww), (0.23 * wh))
    )
    new_userImage = ctk.CTkImage(
        light_image=Image.open(ON_user_profile),
        size=((0.2 * ww), (0.35 * wh))
    )
    adminPart.configure(image = new_adminImage)
    userPart.configure(image = new_userImage)
    bottomLabel.configure(text="Please tap your library card to confirm.")


def completeTransaction(RFID, content, root):
    global bookID, purpose, Title, ww, wh

    pop_up_page = tk.Frame(content, width=500, height=300, bg="#89AEFF")
    pop_up_page.pack(fill="both", expand=True)
    
    left_border = tk.Frame(pop_up_page, width=5, height=300, bg="white")
    left_border.place(x=0, rely=0, relheight=1)
    # Bind the frame touch event, passing the frame as an argument
    pop_up_page.bind("<Button-1>", lambda event: on_frame_touch(event, pop_up_page, content, root))

    pop_up_label = tk.Label(pop_up_page, text=f'"{Title}"', fg="white", font=("Arial", 55, "bold"), 
                            bg="#89AEFF", wraplength=1500)
    pop_up_label.place(relx=0.5, rely=0.45, anchor="center")

    pop_up_label2 = tk.Label(pop_up_page, text="Please touch the screen to continue", fg="white", 
                             font=("Arial", 20, "bold"), bg="#89AEFF")
    pop_up_label2.place(relx=0.5, rely=0.90, anchor="center")

    if purpose == "Borrow":
        Date_Borrowed = datetime.now()
        Deadline = (Date_Borrowed + timedelta(days=3)).date()
        addBorrowBook(RFID, bookID, Date_Borrowed, Deadline, None)

        pop_up_label3 = tk.Label(pop_up_page, text=f'Please return the book on or before {Deadline} to avoid being penalized.', 
                                 fg="white", font=("Arial", 30), bg="#89AEFF", wraplength=2000)
        pop_up_label3.place(relx=0.5, rely=0.60, anchor="center")

        pop_up_label4 = tk.Label(pop_up_page, text='You borrowed', fg="white", font=("Arial", 55, "bold"), 
                                 bg="#89AEFF")
        pop_up_label4.place(relx=0.5, rely=0.30, anchor="center")

        print("Added to the database")
    
    elif purpose == "Return":
        Date_Returned = datetime.now()
        returnBook(RFID, bookID, Date_Returned)

        pop_up_label5 = tk.Label(pop_up_page, text='You returned', fg="white", font=("Arial", 55, "bold"), 
                                 bg="#89AEFF")
        pop_up_label5.place(relx=0.5, rely=0.30, anchor="center")

def on_frame_touch(event, frame, content, main):
    global initialUser
    if event.widget == frame:
        Main_borrow_return_page(content, initialUser, main)
def is_rfid_scan():
    global last_scan_time
    current_time = time.time()
    if current_time - last_scan_time < 1:
        last_scan_time = current_time
        return True
    last_scan_time = current_time
    return False


def keyPressed(event, content, root):
    global rfid_data, bookID, adminRFID, userRFID, initialUser, inst_label
    
    #if not is_rfid_scan():
        #return  # Ignore manual keyboard input
    print("pressed key")
    if event.keysym == "Return":
        if rfid_data and bookID == None:
            print("RUNNING HERE")
            string_data = str(rfid_data)
            save_input(rfid_data, inst_label, content, root)
        if rfid_data and bookID:
            string_data = str(rfid_data)
            print(adminCheck(string_data), string_data)
            if adminCheck(string_data):
                print(f"ADMIN Entered")
                adminRFID = True
                getUser()
                return
            else:
                errorNotif("Admin not found", content, root)
            rfid_data = ""  # Reset buffer
        elif rfid_data and adminRFID:
            user = getUserInfo(rfid_data)
            if user == ([], [], []) or user[0][0][0] == initialUser:
                root.unbind("<Key>")
                successNotif("please wait for the Pop-up screen", content, root)
                root.after(100, lambda: completeTransaction(rfid_data, content, root))
                print(f"User Entered: {user[0][0][1]}")
                return
            else:
                rfid_data = ""
                errorNotif("Incorrect User", content, root)
    else:
        rfid_data += event.char