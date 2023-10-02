from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip as p
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = ''.join(password_list)
    password_i.delete(0, END)
    password_i.insert(0, password)
    p.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_entry():
    email = email_i.get()
    password = password_i.get()
    website = website_i.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0:
        messagebox.showerror('Website', 'Enter the website!')
    elif len(password) == 0:
        messagebox.showerror(website, 'Enter your password!')
    else:
        try:
            with open('data.json', 'r') as data_file:
                # reading data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                # creating new JSON object with new_data inside, dumping to a newly created file
                json.dump(new_data, data_file)
        else:
            # updating data with new data (a dict containing user input)
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_i.delete(0, END)
            password_i.delete(0, END)


# ---------------------------- FIND PASSWORD -------------------------- #

def find_password():
    website = website_i.get()
    try:
        with open('data.json', 'r') as data_file:
            # reading data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror('Database is empty', 'You have no saved passwords. Add passwords first.')
    else:
        if website in data:
            messagebox.showinfo('Password found', f'Website: {website}\nEmail: {data[website]["email"]}\n'
                                              f'Password: {data[website]["password"]}')
        else:
            messagebox.showinfo(f'Unknown website: {website}', f'No details for {website} exist.')
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=189)
bg_pic = PhotoImage(file='logo.png')
canvas.create_image(100, 95, image=bg_pic)
canvas.grid(row=0, column=1)

website_l = Label(text='Website:')
website_l.grid(row=1, column=0)

email_l = Label(text='Email/Username:')
email_l.grid(row=2, column=0)

password_l = Label(text='Password:')
password_l.grid(row=3, column=0)

website_i = Entry(width=27)
website_i.grid(row=1, column=1)
website_i.focus()

email_i = Entry(width=46)
email_i.grid(row=2, column=1, columnspan=2)
email_i.insert(0, 'partyka.bartlomiej3000@gmail.com')

password_i = Entry(width=27)
password_i.grid(row=3, column=1)

genpass_btn = Button(text='Generate Password', width=15, command=generate_password)
genpass_btn.grid(row=3, column=2)

save_btn = Button(text='Save Password', width=39, command=save_entry)
save_btn.grid(row=4, column=1, columnspan=2)

search_btn = Button(text='Search', width=15, command=find_password)
search_btn.grid(row=1, column=2)

window.mainloop()
