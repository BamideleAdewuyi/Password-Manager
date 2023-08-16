from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    new_password = "".join(password_list)

    # Clear password entry box and enter newly generated password
    password_entry.delete(0, END)
    password_entry.insert(END, f"{new_password}")

    # Use pyperclip to automatically copy password to clipboard
    pyperclip.copy(new_password)

# ---------------------------- SEARCH JSON ------------------------------- #
def find_password():
    # Get website user is searching for
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="No data file found", message="No data file found")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Username: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="No website found", message="No details for the website exist")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": username,
        "password": password
    }
    }

    if len(website) == 0 or len(password) == 0:
        # If there are empty entries
        messagebox.showerror(title="Error", message="Please don't leave any fields empty")
    else:
        # Open the password txt file and append info that user has typed in
        # Using a JSON file in read mode first
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        
        # If this json file does not exist. Create it
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
            # Delete info from website and password entries
            website_entry.delete(0, END)
            password_entry.delete(0, END)
        
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
# Create photo image for logo
logo_img = PhotoImage(file="passwordManagerLogo.png")
# Create canvas
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Create labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Create entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
# Using focus method will make it so the cursor is in the website entry box as soon as the window is opened
# so there is no need to click the box in order to start typing
website_entry.focus()
username_entry = Entry(width=30)
username_entry.grid(column=1, row=2, columnspan=2)
# Use insert method to have email address already in box. So no need to type same email every time
username_entry.insert(END, "person@email.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Create buttons
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
gen_password = Button(text="Generate Password", command=generate_password)
gen_password.grid(column=2, row=3)
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1)





window.mainloop()