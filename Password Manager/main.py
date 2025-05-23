from tkinter import *
from tkinter import messagebox
import random
import pyperclip # type: ignore
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password = ""
    for _ in range(0, 10):
        password += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()")
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} " f"\nPassword: {password} \nIs it ok to save?")
        
        if not is_ok:
            return
    try:
        with open("data.json", "r") as data_file:
            # Reading old data
            data = json.load(data_file)
            # Updating old data with new data
            data.update(new_data)
        with open("data.json", "w") as data_file:
            # Saving updated data
            json.dump(data, data_file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)

    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    except KeyError:
        messagebox.showinfo(title="Error", message=f"No details for the {website} exists.")
    else:
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, columnspan=2, sticky="W")
website_entry.focus()

email_entry = Entry(width=43)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "ahmed2005taher@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1, sticky="W")

# Buttons
generate_password_button = Button(text="Generate Password", width= 15, command=generate_password)
generate_password_button.grid(row=3, column=2 , sticky="W")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2, sticky="W")

window.mainloop()