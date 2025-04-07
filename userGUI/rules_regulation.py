import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import pytz  # Import pytz for timezone handling
def create_rounded_frame(parent, width, height, radius=20):
    round_canvas = tk.Canvas(parent, width=width, height=height, bd=0, highlightthickness=0)
    
    # ROUNDED FRAME CODE
    round_canvas.create_arc(
        (0, 0, radius * 2, radius * 2), start=90, extent=90, outline="", fill="white")  # top-left corner
    round_canvas.create_arc(
        (width - radius * 2, 0, width, radius * 2), start=0, extent=90, outline="", fill="white")  # top-right corner
    round_canvas.create_arc(
        (0, height - radius * 2, radius * 2, height), start=180, extent=90, outline="", fill="white")  # bottom-left corner
    round_canvas.create_arc(
        (width - radius * 2, height - radius * 2, width, height), start=270, extent=90, outline="", fill="white")  # bottom-right corner
    round_canvas.create_rectangle(
        radius, 0, width - radius, height, outline="", fill="white")  # top edge
    round_canvas.create_rectangle(
        0, radius, width, height - radius, outline="", fill="white")  # right edge
    return round_canvas

def create_navigation_buttons(content):
    ww = content.winfo_screenwidth()  
    wh = content.winfo_screenheight()
    button_frame = ctk.CTkFrame(content, width=(0.50 * ww), height=80)  # Set width and height in the constructor
    button_frame.place(relx=0.5, rely=0.89, anchor="center")  # Center the button frame at the bottom

    # Button list
    button_texts = ["Rules and Regulations", "Borrowing Privileges", "Fines and Offenses", "Lost Book", "Library Decorum"]

    # Create buttons and ensure equal spacing
    for idx, text in enumerate(button_texts):
        button = ctk.CTkButton(button_frame, text=text, font=("Arial", 19, "bold"), fg_color="#004AAD", width=216, height=60)
        button.pack(side='left', padx=15, expand=True)  # Side by side, with equal padding

    # Assign functions to buttons
    button_frame.winfo_children()[0].configure(command=lambda: Main_rules_page(content))
    button_frame.winfo_children()[1].configure(command=lambda: show_borrowing_privileges_page(content))
    button_frame.winfo_children()[2].configure(command=lambda: show_fno_page(content))
    button_frame.winfo_children()[3].configure(command=lambda: show_lb_page(content))
    button_frame.winfo_children()[4].configure(command=lambda: show_decor_page(content))

def Main_rules_page(content):
    for widget in content.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    ww = content.winfo_screenwidth()
    wh = content.winfo_screenheight()
    time_border = ctk.CTkFrame(content, width=(0.08 * ww), height=(0.067 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    time_border.place(relx=0.89, rely=0.05)

    date_border = ctk.CTkFrame(content, width=(0.13 * ww), height=(0.069 * wh), fg_color="azure3", 
                      corner_radius=13, border_width=15, border_color="azure3")
    date_border.place(relx=0.03, rely=0.05)

    def update_date():
        try: 
            ph_timezone = pytz.timezone("Asia/Manila")
            current_time = datetime.now(ph_timezone)
            formatted_date = current_time.strftime("%B %d, %Y")
            formatted_time = current_time.strftime("%I:%M %p")
            date_label.configure(text=formatted_date)
            time_label.configure(text=formatted_time)
            content.after(1000, update_date)
        except tk.TclError:
        # Widget has been destroyed, stop updating
            return

    date_label = ctk.CTkLabel(date_border, font=("Arial", 24, 'bold'), text_color="Black")
    date_label.place(relx=0.5, rely=0.5, anchor = "center") 

    time_label = ctk.CTkLabel(time_border, font=("Arial", 24, 'bold'), text_color="Black")
    time_label.place(relx=0.5, rely=0.5, anchor = "center") 
    update_date()
    round_canvas1 = create_rounded_frame(content, width=1200, height=600)  
    round_canvas1.place(relx=0.5, rely=0.46, anchor="center")  # Centered

    # FRAME LABEL
    label1 = tk.Label(round_canvas1, text="Library Policies & Regulations", font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label1.place(relx=0.02, rely=0.05)  # Relative placement for better responsiveness

    # POLICIES TEXT
    policies_text = """• No school ID, No proper uniform, No Entry policy is implemented.
• All library users must register by tapping a validated school ID on the RFID reader 
  or signing the statistics form upon entering the library.
• Bags and belongings must be placed at the Bag Counter in library areas with an open-shelf system.
• The library is not responsible for lost belongings left at the bag counter.
• A validated school ID and Library Card are required for borrowing materials.
• Library materials must be borrowed personally.
• Library Cards are non-transferable; misuse will be reported to the Office of Student Discipline.
• Photocopying or taking digital snapshots of theses, research papers, and reports is strictly prohibited.
• Books and materials cannot be borrowed for overnight use a week before final exams."""

    # Text Widget without border, placed using relx/rely
    text_widget = tk.Text(round_canvas1, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0)  
    text_widget.insert(tk.END, policies_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(relx=0.02, rely=0.16, relwidth=0.96, relheight=0.75)  # Adjusted placement
    create_navigation_buttons(content)

# BORROW PAGE
def show_borrowing_privileges_page(content):
    # ROUNDED FRAME VARIABLE
    round_canvas2 = create_rounded_frame(content, width=1200, height=600)  # Corrected width and height
    round_canvas2.place(relx=0.5, rely=0.46, anchor="center")  # Center the frame within the window
    # FRAME LABEL
    label2 = tk.Label(round_canvas2, text='Borrowing Privileges', font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label2.place(relx=0.02, rely=0.05)   # Top-left cornershow_decor_page (0)
    #BORROWING TEXT
    borrowing_text = """• Circulation Books 
    - Students: 2 books—2 days
    - Faculty members: 5 books—2 weeks
    - Non-teaching staff: 3 books—2 weeks
    • Two (2) reserve books can be borrowed at a time for photocopying or library use, one (1) reserve book for overnight starting 1:00pm to be returned on or before 10:00am the following day. 
    • Borrowers are only allowed to renew book/s if the material is not in demand.
    • General reference books, serials, theses, narrative reports, and research works are strictly for library use and may not be photocopied.
    """
    # Text Widget without border
    text_widget = tk.Text(round_canvas2, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0)  
    text_widget.insert(tk.END, borrowing_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(relx=0.02, rely=0.16, relwidth=0.96, relheight=0.75)  # Adjusted placement

# FINES AND OFFENSES
def show_fno_page(content):

    # ROUNDED FRAME VARIABLE
    round_canvas3 = create_rounded_frame(content, width=1200, height=600)  # Corrected width and height
    round_canvas3.place(relx=0.5, rely=0.46, anchor="center")  # Center the frame within the window
    # FRAME LABEL
    label3 = tk.Label(round_canvas3, text='Fines', font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label3.place(relx=0.02, rely=0.05) # Top-left corner
    #fines TEXT
    f_text = """Materials returned late are subject to overdue fines

• General Circulation books
- Php 10.00 per day (Sundays and holidays inclusive)

• Reserve Books
- Php 2.00 for the first hour
- Php 1.00 for every succeeding hour (Inclusion of 
Sundays and holidays)

NOTE:
Payment should be made at the Cashier's Office."""

    # Text Widget without border, placed using relx/rely
    text_widget = tk.Text(round_canvas3, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0)  
    text_widget.insert(tk.END, f_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(relx=0.02, rely=0.16, relwidth=0.96, relheight=0.75)  # Adjusted placement
    
    # FRAME LABEL
    label4 = tk.Label(round_canvas3, text='Offenses', font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label4.place(x=(620), y=(30))  # Top-left corner
    #offenses TEXT
    o_text = """1st offense: fine as directed

2nd offense: fine and one week suspension 
from library privileges

3rd offense: fine and one month suspension 
from library privileges

NOTE: Borrowers with overdue books or unsettled 
accounts to the library will not be allowed to 
borrow/renew any library materials."""
    # Text Widget without border
    text_widget = tk.Text(round_canvas3, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0)  
    text_widget.insert(tk.END, o_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(x=630, y=90)  # Adjust placement inside canvas
    # LOST BOOK PAGE
def show_lb_page(content):
    # ROUNDED FRAME VARIABLE
    round_canvas3 = create_rounded_frame (content, width=1200, height=600)  # Corrected width and height
    round_canvas3.place(relx=0.5, rely=0.46, anchor="center")  # Center the frame within the window
    # FRAME LABEL
    label3 = tk.Label(round_canvas3, text='Lost Book', font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label3.place(relx=0.02, rely=0.05)  # Top-left corner
    #BORROWING TEXT
    borrowing_text = """
    - Lost book must be reported immediately to the librarian and shall be replaced within
    2 weeks. 

    - The said material should be replaced with the later edition of the same book or book 
    of related subject with latest copyright date. 

    - The corresponding fines and processing fee of Php 50.00 must be paid at the 
    Cashier's Office.
    """
    # Text Widget without border
    text_widget = tk.Text(round_canvas3, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0)  
    text_widget.insert(tk.END, borrowing_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(relx=0.02, rely=0.16, relwidth=0.96, relheight=0.75)  # Adjusted placement

def show_decor_page(content):
    # ROUNDED FRAME VARIABLE
    round_canvas4 = create_rounded_frame(content, width=1200, height=600)  # Corrected width and height
    round_canvas4.place(relx=0.5, rely=0.46, anchor="center")  # Center the frame within the window
    # FRAME LABEL
    label4 = tk.Label(round_canvas4, text='Decorum in the Library', font=("Arial", 25, "bold"), 
                      fg="#004AAD", bg="white")
    label4.place(relx=0.02, rely=0.05)  # Top-left corner
    # POLICIES TEXT
    decor_text = """• Observe silence at all times

• Unnecessary noise, loud conversation/ discussion, eating, drinking, sleeping, and playing
games are strictly prohibited.

• Cellular phones and other electronic gadgets must be set to silent mode while inside the 
library. Making/answering calls should be done outside the library.

• Charging of cellphones, laptops and other personal gadgets is not allowed.

• Wearing of hats, caps and the likes is discouraged for courtesy reason. """

    # Text Widget without border
    text_widget = tk.Text(round_canvas4, wrap=tk.WORD, font=("Arial", 17, "bold"), 
                          bg="white", spacing1=10, bd=0, highlightthickness=0) 
    text_widget.insert(tk.END, decor_text)
    text_widget.config(state=tk.DISABLED)  # Make text widget read-only
    text_widget.place(relx=0.02, rely=0.16, relwidth=0.96, relheight=0.75)  # Adjust placement inside canvas
def initiateMainReg(content):
    Main_rules_page(content)
#BORROW RULES
#FINES
#OFFENSES
#LOST BOOK
#DECORUM