from tkinter import *
from tkinter import messagebox
from project import *
from save import SaveFile
import pyperclip
import random

REGED = True
LOGIN = True

class Website:
    def __init__(self, site):
        self._website_name = site
        self.accounts = []

class ClipboardLabel(Label):
    def __init__(self, master, text, data, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.data = data
        self.bind("<Button-1>", self.copy_to_clipboard)

    def copy_to_clipboard(self, event):
        pyperclip.copy(self.data)
        # Optional: Inform user that text was copied

class AccountFrames(Frame):
    def __init__(self, master, account_no, file,**kwargs):
        super().__init__(master, **kwargs)
        self._accountno = account_no
        self.file = file
        self.menu = Menu(self)
        self.menu.add_command(label="Delete", command=self.delete_label)
        self.menu.add_command(label="Edit", command=self.edit_label)
        self.bind("<Button-3>", self.open_menu)

    def open_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def delete_label(self, account, password):
        pass
        # messagebox.askokcancel(title="Warning", message=f"Are you sure you want to delete account {}")
def main():
    pass

def websites():
    global accounts
    data = decrypt(file, passwrd)
    prev = None
    accounts = []
    for i, user in enumerate(data):
        if user["Website"] != prev:
            web = Website(user["Website"])
            accounts.append(web)
            prev = user["Website"]
            website_list.insert(i, user["Website"])
        web.accounts.append({"Username": user["Username"], "Password": user["Password"]})
        
def on_click(event):
    global selected_item
    selected_index = website_list.curselection()
    if selected_index:
        selected_item = website_list.get(selected_index[0])
        load_labels(selected_item)
        home_frame.pack_forget()
        web_frame.pack()

def load_labels(selected_item):
    global account_frames
    i = 0
    title = Label(web_frame,text=selected_item, font=("Arial Black", 18))
    title.grid(row=0, column=0, sticky="n", columnspan=2)
    account_frames = [title]
    context_menu = Menu(web_frame, tearoff=0)
    for account in accounts:
        if account._website_name == selected_item:
            for i, user in enumerate(account.accounts):

                # Frame for each account for the website
                account_frame = Frame(web_frame)
                Label(account_frame, text=f"Account {i + 1}", anchor="w").grid(row=i * 2, column=0, sticky="w")

                # Username label
                username_label = ClipboardLabel(account_frame,
                                       text=f"Username: {user['Username']}", data=user['Username'],
                                       anchor="w",
                                       width=20)
                username_label.grid(row=i * 2 + 1, column=0, sticky="w")

                # Password label
                password_label = ClipboardLabel(account_frame,
                                       text=f"Password: {user['Password']}", data=user['Password'],
                                       anchor="w",
                                       width=20)
                password_label.grid(row=i * 2 + 2, column=0, sticky="w")
                Label(account_frame, text="").grid(row=i * 2 + 3, column=0)
                account_frame.grid(row=i * 2 + 1, column=0)
                account_frames.append(account_frame)

    # Back button
    back_button = Button(web_frame, text="Back", command=back_to_home)
    back_button.grid(row=i * 2 + 3, column=1)
    account_frames.append(back_button)

    # Add account
    add_account_button = Button(web_frame, text="Add account", command=lambda s=selected_item: add_an_account_in_website(s))
    add_account_button.grid(row=i * 2 + 3, column=0)
    account_frames.append(add_account_button)

def back_to_home():
    web_frame.pack_forget()
    website_list.delete(0, END)
    accounts = []
    for frame in account_frames:
        frame.grid_forget()
    websites()
    home_frame.pack()
    website_list.pack()

def add_an_account_in_website(website_name):
    for frame in account_frames:
        frame.grid_forget()
    add_acc_web_frame = Frame(web_frame)
    # Username entry
    add_username = Entry(add_acc_web_frame)
    add_username.grid(row=1, column=0)
    account_frames.append(add_username)

    # Password entry
    add_password = Entry(add_acc_web_frame)
    add_password.grid(row=2, column=0)
    account_frames.append(add_password)

    generate_pass = Button(add_acc_web_frame,
                           text="Generate password",
                           command=lambda a=add_password: gen_pass(a))
    generate_pass.grid(row=2, column=1)
    account_frames.append(generate_pass)

    save_button = Button(add_acc_web_frame,
                         text="Submit account",
                         command=lambda wn=website_name, au=add_username, ap=add_password: save_account(wn, au, ap))
    save_button.grid(row=3, column=0, columnspan=2)
    account_frames.append(save_button)

    add_acc_web_frame.grid(row=0, column=0)

def save_account(website_name, add_username, add_password):
    new_pass = add_password.get()
    new_name = add_username.get()
    add_account(file, passwrd, website_name, new_name, new_pass)

    back_to_home()
    
    
def gen_pass(add_password):
    global generated_pass
    length = random.randint(9,13)
    generated_pass = generate_password(length)
    add_password.delete(0, END)
    add_password.insert(0, generated_pass)

def login_screen():
    home_frame.pack_forget()
    login_frame.pack()

def login():
    # Add logic to check if login is correct
    global usernme
    global file
    global passwrd
    usernme = username.get()
    passwrd = password.get()
    file = SaveFile(usernme)
    users = file.load_user_config()
    for user in users['Users']:
        if user['Username'] == username.get():
            if validate_password(file, password.get()):
                login_success()
                return
            else:
                login_failed()
                return
        else:
            continue
    not_registered()

def show_pass():
    password.config(show="")
    show_password.pack_forget()
    hide_password.pack()

def hide_pass():
    password.config(show="*")
    hide_password.pack_forget()
    show_password.pack()

def login_success():
    login_frame.pack_forget()
    home_frame.pack()
    websites()

def login_failed():
    global LOGIN
    if LOGIN:
        noaccount = Label(login_frame,
            text="Invalid password")
        noaccount.pack()
        LOGIN = False


def not_registered():
    global REGED
    if REGED:
        noaccount = Label(login_frame,
            text="This user does not exist. Please register")
        noaccount.pack()
        REGED = False

def register():
    login_frame.pack_forget()
    # registration_frame.pack()

if __name__ == "__main__":
    window = Tk()
    window.title("Password manager")
    # Login page
    login_frame = Frame(window)
    username = Entry(login_frame,
                        font=("Arial", 15))
    username.pack()
    password = Entry(login_frame,
                font=("Arial", 15),
                show="*")
    password.pack()
    login_but = Button(login_frame,
                text="Login",
                command=login)
    login_but.pack()
    register_but = Button(login_frame,
                          text="Register",
                          command=register)
    register_but.pack()
    show_password = Button(login_frame,
                           text="Show password",
                           command=show_pass)
    show_password.pack()
    hide_password = Button(login_frame,
                           text="Hide password",
                           command=hide_pass)
    # Registration page

    # Home page
    home_frame = Frame(window)
    website_list = Listbox(home_frame,
                           font=("Arial", 12))
    website_list.pack()
    website_list.bind("<ButtonRelease-1>", on_click)

    # Website accounts
    web_frame = Frame(window)


    login_screen()

    window.mainloop()
