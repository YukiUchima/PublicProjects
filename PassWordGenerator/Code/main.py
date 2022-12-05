from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, END
import json
import pyperclip
from random import randint, choice, shuffle
from string import ascii_letters, punctuation, digits

CURRENT_FILE = "login_data.json"
# Find website and its information
def search():
    website = websiteEntry.get().casefold()
    if website:
        try:
            with open(CURRENT_FILE, "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as err:
            messagebox.showinfo(title="Not Found", message="There was no entry found for the website")
        else:
            try:
                password_info = data[website]["password"]
                email_info = data[website]["email"]
            except KeyError:
                messagebox.showinfo(title="Missing Entry", message="Missing website entry in database")
            else:
                messagebox.showinfo(title="Login Information", message=f"Website: {website}\n\tLogin: {email_info}\n\tPassword: {password_info}")
            finally:
                pyperclip.copy(password_info)
# Add to JSON file
def addInfo():
    if not websiteEntry.get() or not pwEntry.get():
        messagebox.showinfo(title="Error", message="Enter valid entries for text fields")
    else:
        website = websiteEntry.get().casefold()
        email = contactEntry.get().casefold()
        password = pwEntry.get()

        new_data_entry = {
            website: {
                "email": email,
                "password": password,
            }
        }

        try:
            # Attempt to read file only if it already exists
            with open(CURRENT_FILE, "r") as data_file:
                cur_data = json.load(data_file)
        except FileNotFoundError:
            # If file doesn't exist, creates and adds new entry
            with open(CURRENT_FILE, "w") as data_file:
                json.dump(new_data_entry, data_file, indent=4)
        else:
            # Continues to update if no exception is raised
            cur_data.update(new_data_entry)
            with open(CURRENT_FILE, "w") as data_file:
                json.dump(cur_data, data_file, indent=4)
        finally:
            websiteEntry.delete(0, END)
            pwEntry.delete(0, END)


# Generate a new Password
def genPW():
    letter_list = [choice(ascii_letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(punctuation) for _ in range(randint(2, 4))]
    number_list = [choice(digits) for _ in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list
    shuffle(password_list)
    password = "".join(password_list)
    pwEntry.delete(0, END)
    pwEntry.insert(0, password)
    pyperclip.copy(password)

# HOVER color changing function
def changeOnHover(btn, colorOnHover, color):
    btn.bind("<Enter>", func=lambda e: btn.config(background=colorOnHover))
    btn.bind("<Leave>", func=lambda e: btn.config(background=color))

# ---------------------------- UI SETUP ------------------------------- #
GREEN = '#004522'

window = Tk()
window.title("PW Manager")
window.config(padx=20, pady=20, bg='BLACK')

canvas = Canvas(width=200, height=200, bg='BLACK', highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=0, columnspan=3)

# Label -----------------------------------------
websiteLabel = Label(text="Website:", bg='BLACK', fg='WHITE', font="Courier 10")
websiteLabel.grid(row=1, column=0, sticky="EW", pady=(0, 10))
contactLabel = Label(text="Email/Username:", bg='BLACK', fg='WHITE', font="Courier 10")
contactLabel.grid(row=2, column=0, sticky="EW", pady=(0, 10))
pwLabel = Label(text="Password:", bg='BLACK', fg='WHITE', font="Courier 10")
pwLabel.grid(row=3, column=0, sticky="EW", pady=(0, 10))

# ENTRIES ---------------------------------------
websiteEntry = Entry()
websiteEntry.grid(row=1, column=1, sticky="EW", pady=(0, 10))
websiteEntry.focus()
contactEntry = Entry(width=35)
contactEntry.grid(row=2, column=1, columnspan=3, sticky="EW", pady=(0, 10))
contactEntry.insert(0, '@gmail.com')
pwEntry = Entry()
pwEntry.grid(row=3, column=1, sticky="EW", pady=(0, 10))

# BUTTON ----------------------------------------
addBtn = Button(text="Add", width=35, bg='#008E8C', fg='WHITE', font="Courier 10", highlightthickness=0, command=addInfo)
addBtn.grid(row=4, column=1, columnspan=2, sticky="EW")
genPWBtn = Button(text="Generate Password", width=17, bg='#008E8C', fg='WHITE', font="Courier 8", highlightthickness=1, command=genPW)
genPWBtn.grid(row=3, column=2, sticky="NE")
searchBtn = Button(text="Search", width=17, bg='#008E8C', fg='WHITE', font="Courier 8", highlightthickness=1, command=search)
searchBtn.grid(row=1, column=2, sticky="NE")

# BUTTON HOVER CHANGE ---------------------------
changeOnHover(searchBtn, "#00605E", "#008E8C")
changeOnHover(genPWBtn, "#00605E", "#008E8C")
changeOnHover(addBtn, "#00605E", "#008E8C")

window.mainloop()