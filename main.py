from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- CONSTANTS ------------------------------- #
DEFAULT_EMAIL = "wjoshbruton@gmail.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
               'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    passwd_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = website_entry.get()
    usrname = usrname_entry.get()
    passwd = passwd_entry.get()
    new_data = {
        website: {
            "email": usrname,
            "password": passwd,
        }
    }

    if len(website) == 0 or len(passwd) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askyesno(title=website,
                                    message=f"These are the details entered for {website}: \n\n\tEmail/Login: {usrname}"
                                            f"\n\tPassword: {passwd} \n\nIs it okay to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                usrname_entry.delete(0, END)
                usrname_entry.insert(0, DEFAULT_EMAIL)
                passwd_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# ---------------------------- LOGO CANVAS ------------------------------- #
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# ---------------------------- LABELS------------------------------- #
website_lbl = Label(window, text="Website:")
website_lbl.grid(column=0, row=1)

usrname_lbl = Label(window, text="Email/Username:")
usrname_lbl.grid(column=0, row=2)

passwd_lbl = Label(window, text="Password:")
passwd_lbl.grid(column=0, row=3)

# ---------------------------- ENTRY ------------------------------- #
usrname_entry = Entry(window, width=40)
usrname_entry.grid(column=1, row=2, columnspan=2)
usrname_entry.insert(0, DEFAULT_EMAIL)

website_entry = Entry(window, width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

passwd_entry = Entry(window, width=21)
passwd_entry.grid(column=1, row=3)

# ---------------------------- BUTTONS ------------------------------- #
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

gen_pass_btn = Button(text="Generate Password", command=gen_pass)
gen_pass_btn.grid(column=2, row=3)

add_btn = Button(text="Add", width=36, command=save_pass)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()
