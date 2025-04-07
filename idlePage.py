import tkinter as tk
from userGUI.mainGUI import start_neuread_app
from userGUI.adminPanel import admin
import time
import datetime
from bnd import *
from PIL import Image, ImageTk
# Create the main application window
root = tk.Tk()
root.title("Idle Page")
root.attributes('-fullscreen', True)
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight() 
last_scan_time = 0
active = False
rfid_data = "0010516239"
def create_idle_page():
    """Creates the idle page UI."""
    global idle_frame
    bg_image = Image.open("idlePage.png")
    bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    idle_frame = tk.Frame(root, width=500, height=300, bg="lightgray")
    idle_frame.pack(fill="both", expand=True)
    bg_label = tk.Label(idle_frame, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)
    WhoToPenalize()#Penalize kung sino need
    # Bind key events to capture RFID input
    root.bind("<Key>", on_key_press)

def return_to_idle():
    global active
    """Returns the user to the idle page by clearing the screen and recreating the idle frame."""
    for widget in root.winfo_children():
        widget.destroy()
    active = False  
    create_idle_page()

def on_key_press(event):
    global active
    global rfid_data
    global idle_frame
    if active:
        return
    if event.keysym == "Return":
        print("pressing")
        if rfid_data:
            if getUserInfo(rfid_data) != ([], [], []):
                try:
                    if getUserInfo(rfid_data)[0][0][2] == "Admin":
                        root.unbind("<Key>")
                        rfid_data = ""  # Reset buffer
                        admin(root, return_to_idle, root)
                    else:
                        active = True
                        print(f"RFID Scanned: {rfid_data}")
                        root.unbind("<Key>")
                        start_neuread_app(rfid_data, root, return_to_idle)
                        print(rfid_data)
                        
                        rfid_data = ""  # Reset buffer
                        idle_frame.destroy()
                except Exception as e:
                    rfid_data = ""
                    return None
            else:
                rfid_data = ""
                print("no user as such")
    else:
        rfid_data += event.char
        print(rfid_data)
def check_time():
    """Checks the current time and runs showWhoToEmail() if it's between 4:00 PM and 4:15 PM."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    if "16:00" <= current_time <= "16:15":  # Check if it's between 4:00 and 4:15 PM
        print("Running showWhoToEmail()...")
        showWhoToEmail()

    root.after(60000, check_time)  # Schedule the function to run again in 1 minute

# Initialize the idle page at startup
create_idle_page()
check_time()
# Run the application
root.mainloop()

