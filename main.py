import json
import random
import string
import tkinter as tk
from tkinter import messagebox
import emoji
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from json import JSONDecodeError

DEFAULT_EMAIL = "youremail@gmail.com"

# Globals to track references
password_entry = None
eye_btn = None
password_shown = False
pending_data = {}
notebook = None

# We'll store references for the password database GUI elements
password_db_frame = None     # Container frame (holds canvas + scrollbar)
db_canvas = None             # Canvas for scrolling
db_content_frame = None      # Actual frame to hold the database items

# Emojis for open/closed "eye"
eye_open_emoji = emoji.emojize(":monkey_face:")
eye_closed_emoji = emoji.emojize(":see_no_evil_monkey:")


def load_password_db():
    """
    Loads all entries from data.json and displays them on the 'db_content_frame'
    in an organized format:
        ------------------------------------
        Website: ...
        Username: ...
        Password: ...
        ------------------------------------
    """
    # Clear anything that was previously on this frame
    for widget in db_content_frame.winfo_children():
        widget.destroy()

    # Attempt to read existing data
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        data = {}  # No data or invalid JSON => start empty

    # Display each entry
    row_index = 0
    for website, creds in data.items():
        sep_top = tbs.Label(db_content_frame, text="------------------------------------")
        sep_top.grid(row=row_index, column=0, padx=5, pady=2, sticky=tk.W)
        row_index += 1

        w_lbl = tbs.Label(db_content_frame, text=f"Website: {website}")
        w_lbl.grid(row=row_index, column=0, padx=5, sticky=tk.W)
        row_index += 1

        u_lbl = tbs.Label(db_content_frame, text=f"Username: {creds['email']}")
        u_lbl.grid(row=row_index, column=0, padx=5, sticky=tk.W)
        row_index += 1

        p_lbl = tbs.Label(db_content_frame, text=f"Password: {creds['password']}")
        p_lbl.grid(row=row_index, column=0, padx=5, sticky=tk.W)
        row_index += 1

    # Optional: a final separator line at the bottom
    sep_bottom = tbs.Label(db_content_frame, text="------------------------------------")
    sep_bottom.grid(row=row_index, column=0, padx=5, pady=(2, 10), sticky=tk.W)


def confirm_save():
    """
    Called when user clicks "Confirm" in the preview (results) tab.
    Merges 'pending_data' into data.json, refreshes the Password Database tab,
    and switches to it.
    """
    global pending_data

    # Load existing data
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, JSONDecodeError):
        data = {}

    # Merge in the new data waiting to be saved
    data.update(pending_data)

    # Write back to data.json
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    # Clear fields in the form
    website_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    email_entry.insert(0, DEFAULT_EMAIL)
    password_entry.delete(0, tk.END)

    # Clear pending data
    pending_data = {}

    # Refresh the Password Database tab
    load_password_db()
    # Switch to that tab
    notebook.select(password_db_frame)


def cancel_save():
    """
    Called when user clicks "Cancel" in the preview (results) tab.
    Discards 'pending_data' and returns to the form tab.
    """
    global pending_data
    pending_data = {}
    notebook.select(entry_frame)  # Go back to the add/search form


def show_new_entry():
    """
    Called when user clicks the 'Add Website' button.
    1. Validates the fields.
    2. If valid, stores them in 'pending_data'.
    3. Clears/updates the results_frame with the preview of the new entry.
    4. Switches to the results_frame tab so user can Confirm/Cancel.
    """
    website = website_entry.get().strip()
    usrname = email_entry.get().strip()
    passwd = password_entry.get().strip()

    if len(website) == 0 or len(passwd) == 0:
        messagebox.showinfo(
            title="Oops",
            message="Please make sure you haven't left any fields empty."
        )
        return

    global pending_data
    # Prepare new data to be confirmed
    pending_data = {
        website: {
            "email": usrname,
            "password": passwd
        }
    }

    # Clear out any previous preview in results_frame
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Show the user the new entry
    preview_title = tbs.Label(results_frame, text="New Entry Preview", bootstyle=PRIMARY)
    preview_title.pack(pady=5)

    w_label = tbs.Label(results_frame, text=f"Website: {website}")
    w_label.pack(pady=2)

    u_label = tbs.Label(results_frame, text=f"Username: {usrname}")
    u_label.pack(pady=2)

    p_label = tbs.Label(results_frame, text=f"Password: {passwd}")
    p_label.pack(pady=2)

    # Confirm/Cancel buttons
    btn_frame = tbs.Frame(results_frame)
    btn_frame.pack(pady=10)

    confirm_btn = tbs.Button(btn_frame, text="Confirm", bootstyle=SUCCESS, command=confirm_save)
    confirm_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tbs.Button(btn_frame, text="Cancel", bootstyle=DANGER, command=cancel_save)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    # Switch to the results tab to let the user confirm
    notebook.select(results_frame)


def find_password():
    """
    Searches 'data.json' for an entry matching the 'website' field
    and shows the result in a messagebox.
    """
    website = website_entry.get().strip()
    if not website:
        messagebox.showinfo(title="Error", message="Please enter a website name.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
        return
    except JSONDecodeError:
        messagebox.showinfo(title="Error", message="Data file is invalid or empty.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )
    else:
        messagebox.showinfo(
            title="Error",
            message=f"No details for '{website}' exist."
        )


def generate_password():
    """
    Generates a 17-character password consisting of letters, digits, and punctuation,
    and updates the 'password_entry' field.
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    generated = ''.join(random.choice(chars) for _ in range(17))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated)


def toggle_password_view():
    """
    Toggles between hiding and showing the password in 'password_entry',
    and toggles the 'eye_btn' text between open/closed emojis.
    """
    global password_shown
    if not password_shown:
        # Reveal characters
        password_entry.config(show="")
        # Switch to "closed-eye" emoji
        eye_btn.config(text=eye_closed_emoji)
        password_shown = True
    else:
        # Hide characters
        password_entry.config(show="*")
        # Switch to "open-eye" emoji
        eye_btn.config(text=eye_open_emoji)
        password_shown = False


# --------------------- MAIN APPLICATION WINDOW ---------------------
style = tbs.Style(theme="darkly")
root = style.master
root.title("BRu Password Manager")

# --------------------- TOP FRAME & LOGO ---------------------
top_frame = tbs.Frame(root, padding=10)
top_frame.pack(side=tk.TOP, fill=tk.X)

try:
    logo_image = Image.open("images/BRuPassLogo(noBG).png")
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tbs.Label(top_frame, image=logo_photo)
    logo_label.image = logo_photo  # keep a reference to avoid GC
    logo_label.pack()
except Exception as e:
    print("Error loading the logo image:", e)

# --------------------- NOTEBOOK (TABS) ---------------------

notebook = tbs.Notebook(root, padding=10, bootstyle=DEFAULT)
notebook.pack(fill=tk.BOTH, expand=True)

# 1) Create a frame for the "Search Creds" (the main form)

entry_frame = tbs.Frame(notebook)
notebook.add(entry_frame, text="Search Creds")

# 2) Create a frame for the "Search Results" (preview tab)

results_frame = tbs.Frame(notebook)
notebook.add(results_frame, text="Preview Entry")

# 3) Create a frame for the "Password Database"

password_db_frame = tbs.Frame(notebook)
notebook.add(password_db_frame, text="Password Database")

# Now inside 'password_db_frame', we place a canvas + scrollbar + content frame

db_canvas = tk.Canvas(password_db_frame, highlightthickness=0)
db_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tbs.Scrollbar(password_db_frame, orient="vertical", command=db_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

db_canvas.configure(yscrollcommand=scrollbar.set)

# The content frame that we actually populate

db_content_frame = tbs.Frame(db_canvas)
# Create a window inside the canvas to hold 'db_content_frame'
db_canvas.create_window((0, 0), window=db_content_frame, anchor="nw")


# Function to update scroll region when the frame's size changes
def on_frame_configure(event):
    db_canvas.configure(scrollregion=db_canvas.bbox("all"))


db_content_frame.bind("<Configure>", on_frame_configure)

# --------------------- LABELS & ENTRIES: SEARCH CREDS TAB ---------------------
# Row 0: Website
website_label = tbs.Label(entry_frame, text="Website:")
website_label.grid(row=0, column=0, padx=(0, 5), pady=(5, 2), sticky=tk.W)

website_entry = tbs.Entry(entry_frame, width=40)
website_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=(5, 2), sticky=tk.W)

# Row 1: Email/Username + Search Button
email_label = tbs.Label(entry_frame, text="Email/Username:")
email_label.grid(row=1, column=0, padx=(0, 5), pady=(5, 2), sticky=tk.W)

email_entry = tbs.Entry(entry_frame, width=40)
email_entry.grid(row=1, column=1, padx=5, pady=(5, 2), sticky=tk.W)
email_entry.insert(0, DEFAULT_EMAIL)

search_btn = tbs.Button(entry_frame, text="Search", bootstyle=INFO, width=10, command=find_password)
search_btn.grid(row=1, column=2, padx=(10, 5), pady=(5, 2), sticky=tk.W)

# Row 2: Password + Generate Password + Eye Toggle
password_label = tbs.Label(entry_frame, text="Password:")
password_label.grid(row=2, column=0, padx=(0, 5), pady=(5, 2), sticky=tk.W)


password_entry = tbs.Entry(entry_frame, width=40, show="*")
password_entry.grid(row=2, column=1, padx=(5, 0), pady=(5, 2), sticky=tk.W)

generate_btn = tbs.Button(entry_frame, text="Generate Password", bootstyle=PRIMARY, command=generate_password)
generate_btn.grid(row=2, column=2, padx=(10, 5), pady=(5, 2), sticky=tk.W)

# Eye toggle button

eye_btn = tbs.Button(entry_frame, text=eye_open_emoji, bootstyle=LINK, command=toggle_password_view)
eye_btn.grid(row=2, column=1, sticky=tk.E, padx=(0, 25), pady=(5, 2))

# Row 3: Button to show the new entry in the preview (instead of directly saving)
add_btn = tbs.Button(entry_frame, text="Add Website", bootstyle=SECONDARY, command=show_new_entry)
add_btn.grid(row=3, column=1, padx=(10, 5), pady=(5, 10), sticky=tk.S)

# --------------------- INITIAL LOAD OF THE PASSWORD DATABASE ---------------------
load_password_db()

# --------------------- START THE APPLICATION ---------------------
root.mainloop()
