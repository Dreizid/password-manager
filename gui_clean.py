from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from project import *
from save import SaveFile
from fancy_tkinter import *
import pyperclip
import random



class LoginPage(Frame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.packed_frames = []


    def title_part(self):
        # Title
        self.title_frame = Frame(self)
        self.title = Label(self.title_frame, text="Password\nManager", font=("COPPERPLATE GOTHIC BOLD", 30))
        self.title.pack(pady=(20, 20))
        self.title_frame.pack()
        self.packed_frames.append(self.title_frame)

    def input_part(self):
        # Inputs
        font = ("Arial", 12)
        self.entry_frame = Frame(self)
        self.username_entry = LabeledEntry(self.entry_frame, "Username", font=font, width=18)
        self.password_entry = LabeledEntry(self.entry_frame, "Password", font=font, width=13, show="*")
        self._show_password = Button(self.entry_frame, text="show", command=self.password_visibility, font=("Arial", 7), width=6)
        self._hide_password = Button(self.entry_frame, text="hide", command=self.hide_password, font=("Arial", 7), width=6)
        self.username_entry.pack(pady=(15, 5), side="top")
        self._show_password.pack(pady=(10, 5), side="right")
        self.password_entry.pack(pady=(10, 5), side="left")
        self.entry_frame.pack()
        self.packed_frames.append(self.entry_frame)

    def button_part(self):
        # Buttons
        self.button_frame = Frame(self)
        self._login_button = Button(self.button_frame, text="Login", command=self.login, width=9)
        self._register_button = Button(self.button_frame, text="Register", command=self.register, width=9)
        self._login_button.pack(pady=(10, 10), side="right")
        self._register_button.pack(pady=(10, 10), padx=(0, 20), side="left")
        self.button_frame.pack()
        self.packed_frames.append(self.button_frame)

    def misc_part(self):
        # Misc
        self.new_frame = Frame(self)
        self.invalid_user = Label(self.new_frame, text="Username or password doesnt exist!")
        self.invalid_user.pack(pady=(10, 10), side="top")

    def pack_all(self):
        self._TOGGLE_PASSWORD = True
        self._REGISTERED = True
        self.title_part()
        self.input_part()
        self.button_part()
        self.misc_part()
        self.pack(fill="both", expand=True)
        self.color(bg="#1d1e21", tc="#0abf98")

    def login(self):
        self.login_username = self.username_entry.get()
        self.file = SaveFile(self.login_username)
        user_config = self.file.load_user_config()
        for account in user_config["Users"]:
            if account["Username"] == self.login_username:
                self.authenticate()
                return
        if self._REGISTERED:
            self.new_frame.pack()
            self._REGISTERED = False
            self.packed_frames.append(self.new_frame)
        

    def authenticate(self):
        login_password = self.password_entry.get()
        if validate_password(self.file, self.login_password):
            self.login_success(login_password)

    def login_success(self, password):
        self.home_page = HomePage(self.file, password, self.master)

    def register(self):
        for frame in self.packed_frames:
            frame.pack_forget()
        registration_page = RegistrationPage(self)
        registration_page.pack_all_reg()

    def password_visibility(self):
        if self._TOGGLE_PASSWORD and self.password_entry.get() != self.password_entry.placeholder and not self.password_entry.get() == "":
            self.password_entry.config(show="")
            self._show_password.pack_forget()
            self._hide_password.pack(pady=(10, 5), side="right")
            self._TOGGLE_PASSWORD = False
    
    def hide_password(self):
        if not self._TOGGLE_PASSWORD and self.password_entry.get() != self.password_entry.placeholder and not self.password_entry.get() == "":
            self.password_entry.config(show="*")
            self._hide_password.pack_forget()
            self._show_password.pack(pady=(10, 5), side="right")
            self._TOGGLE_PASSWORD = True
            

    def color(self, **kwargs):
        args = kwargs
        self.config(bg=args.get("bg", None))
        self.title.config(bg=args.get("bg", None), fg=args.get("tc", None))
        self.invalid_user.config(bg=args.get("bg", None), fg=args.get("tc", None))
        for frame in self.packed_frames:
            frame.config(bg=args.get("bg", None))

class RegistrationPage(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.packed_frames = []
        self.master = master
    
    def title_part(self):
        # Title
        self.title_frame = Frame(self)
        self.title = Label(self.title_frame, text="Password\nManager", font=("COPPERPLATE GOTHIC BOLD", 30))
        self.title.pack(pady=(20, 20))
        self.title_frame.pack()
        self.packed_frames.append(self.title_frame)

    def entry_part(self):
        # Entry parts
        self.entry_frame = Frame(self)
        self.username = LabeledEntry(self.entry_frame, "Username", font=("Arial", 12), width=18)
        self.password = LabeledEntry(self.entry_frame, "Password", font=("Arial", 12), width=18)
        self.confirm_password = LabeledEntry(self.entry_frame, "Confirm password", font=("Arial", 12), width=18)
        self.username.pack(pady=(15, 5), side="top")
        self.password.pack(pady=(10, 5))
        self.confirm_password.pack(pady=(10, 5))
        self.entry_frame.pack()
        self.packed_frames.append(self.entry_frame)

    def button_part(self):
        # Button parts
        self.button_frame = Frame(self)
        self.register_button = Button(self.button_frame, text="Register", command=self.register_event, width=8)
        self.back_button = Button(self.button_frame, text="Back", command=self.back, width=8)
        self.register_button.pack(pady=(10 ,5), padx=(17, 0), side="right")
        self.back_button.pack(pady=(10, 5), padx=(0, 17), side="left")
        self.button_frame.pack()
        self.packed_frames.append(self.button_frame)

    def invalid_username(self):
        if self._INVALID_USERNAME:
            return
        self.invalid_frame = Frame(self)
        self.error_message = Label(self.invalid_frame, text="Please enter a valid username")
        self.error_message.pack()
        self.invalid_frame.pack()
        self.packed_frames.append(self.invalid_frame)
        self._INVALID_USERNAME = True
        if self._ALREADY_REGED:
            self.already_registered_frame.pack_forget()
            self._ALREADY_REGED = False
            self.packed_frames.append(self.invalid_frame)

    def register_event(self):
        # Registers user
        username = self.username.get()
        password = self.password.get()
        conf_password = self.confirm_password.get()
        if username == "Username" and password == "Password" or password == "Password" and conf_password == "Confirm password":
            self.invalid_username()
        file = SaveFile(username)
        for user in file.load_user_config()["Users"]:
            if user["Username"] == username:
                self.already_registered()
                return
        if password == conf_password:
            filepath = "C:\\Users\Andrei\\Desktop\\VS code\\Users" 
            file.new_user(filepath)
            match_password(file, username)
            

    def already_registered(self):
        if self._ALREADY_REGED:
            return
        self.already_registered_frame = Frame(self)
        self.already_registered_label = Label(self.already_registered_frame, text="Already Registered!")
        self.already_registered_frame.pack()
        self.already_registered_label.pack()
        self._ALREADY_REGED = True
        if self._INVALID_USERNAME:
            self._INVALID_USERNAME = False
            self.invalid_frame.pack_forget()
            self.packed_frames.append(self.already_registered_frame)

    def pack_all_reg(self):
        self._ALREADY_REGED = False
        self._INVALID_USERNAME = False
        self.title_part()
        self.entry_part()
        self.button_part()
        self.pack()
        self.color(bg="#1d1e21", tc="#0abf98") # TO DO: Fix colors

    def back(self):
        self.pack_forget()
        self.master.pack_all()

    def color(self, **kwargs):
        self.title.config(bg=kwargs.get("bg", None), fg=kwargs.get("tc", None))
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None))
        self.config(bg=kwargs.get("bg", None))

class HomePage(Frame):
    def __init__(self, file, password, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file = file
        self.password = password
        self.packed_frames = []
        self.websites_list = Listbox(self, font=("Arial", 14))
        self.websites_list.bind("<ButtonRelease-1>", self.on_click)

    def title_part(self):
        self.title_frame = Frame(self)
        self.title_label = Label(self.title_frame, text=f"Welcome\n{self.file._username}", font=("COPPERPLATE GOTHIC BOLD", 30))
        self.title_label.pack(pady=(20, 20))
        self.title_frame.pack()
        self.packed_frames.append(self.title_frame)

    def page_logic(self):
        data = decrypt(self.file, self.password)
        prev = None
        self.websites = []
        height = 0
        for i, user in enumerate(data):
            if user["Website"] != prev:
                account_page = AccountPage(self.password , self.file, user["Website"], self)
                self.websites.append(account_page)
                prev = user["Website"]
                self.websites_list.insert(i, user["Website"])
                height += 1
            account_page.accounts.append({"Username": user["Username"], "Password": user["Password"]})
        self.websites_list.config(height=height)

    def on_click(self, event):
        selected_index = self.websites_list.curselection()
        if selected_index:
            selected_item = self.websites_list.get(selected_index[0])
            for website in self.websites:
                if website.website == selected_item:
                    self.pack_forget_all()
                    website.pack_all()

    def pack_forget_all(self):
        for frame in self.packed_frames:
            frame.pack_forget()

    def pack_all(self):
        self.title_part()
        self.color(bg="#1d1e21", tc="#0abf98")
        self.websites_list.pack(pady=(10, 10))
        self.packed_frames.append(self.websites_list)
        self.pack()

    def color(self, **kwargs):
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None))
        self.config(bg=kwargs.get("bg", None))
        self.title_label.config(bg=kwargs.get("bg", None), fg=kwargs.get("tc", None))
        self.websites_list.config(bg=kwargs.get("bg", None), fg="white", borderwidth=0, highlightthickness=0, selectbackground="#131416", activestyle="none", width=15)

    

class AccountPage(Frame):

    def __init__(self, password, file, website, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file = file
        self.website = website
        self.password = password
        self.master = master
        self.accounts = []
        self.packed_frames = []

    def scroll(self):
        canvas = Canvas(self, width=280, height=400, borderwidth=0, highlightthickness=0)
        canvas.pack(side=LEFT, fill="both", expand=True)
        scroll_wheel = Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_wheel.pack(side=RIGHT, fill="y")
        canvas.configure(yscrollcommand=scroll_wheel.set)
        canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        self.new_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.new_frame, anchor="nw")
        self.packed_frames.append(self.new_frame)
        self.packed_frames.append(canvas)
        self.packed_frames.append(scroll_wheel)


    def title_part(self):
        self.title_frame = Frame(self.new_frame)
        self.title_label = Label(self.title_frame, text=self.website, font=("COPPERPLATE GOTHIC BOLD", 30))
        self.title_label.pack(pady=(20, 20))
        self.title_frame.pack(padx=(28, 0))
        self.packed_frames.append(self.title_frame)

    def load_labels(self): 
        text_color = "white"
        i = 0
        self.account_frames = []
        self.scroll()
        self.title_part()
        context_menu = Menu(self, tearoff=0)
        for i, account in enumerate(self.accounts):
            account_frame = Frame(self.new_frame)
            account_frame.pack(pady=(0, 30))
            # Frame for each account for the website
            account_no = Label(account_frame, text=f"Account {i + 1}", font=("Arial", 10), anchor="w", fg=text_color)
            account_no.pack()

            # Username label
            username_label = ClipboardLabel(account_frame,
                                            text=f"Username: {account['Username']}", data=account['Username'],
                                            anchor="w",
                                            width=20, font=("Arial", 12),
                                            fg=text_color)
            username_label.pack()

            # Password label
            password_label = ClipboardLabel(account_frame,
                                            text=f"Password: {account['Password']}", data=account['Password'],
                                            anchor="w",
                                            width=20, font=("Arial", 12),
                                            fg=text_color)
            password_label.pack()
            self.packed_frames.append(account_no)
            self.packed_frames.append(username_label)
            self.packed_frames.append(password_label)
            self.packed_frames.append(account_frame)

        # Back button
        back_button = Button(self.new_frame, text="Back", width=8, command=self.back_to_home)
        back_button.pack(side="left", padx=(30,0), pady=(0, 20))
        self.packed_frames.append(back_button)

        # Add account
        add_account_button = Button(self.new_frame, text="Add account", command=lambda s=self.website: self.add_account_page(s))
        add_account_button.pack(side="right", padx=(30,0), pady=(0, 20))
        self.packed_frames.append(add_account_button)

    def back_to_home(self):
        self.forget_all()
        self.master.pack_all()

    def add_account_page(self, event):
        self.forget_all()
        self.pack()
        AddAccountPage(self.file, self.website, self).pack()

    def forget_all(self):
        for frame in self.packed_frames:
            frame.pack_forget()
        self.pack_forget()

    def pack_all(self):
        self.pack() 
        self.load_labels()
        self.color(bg="#1d1e21", tc="#0abf98")

    def color(self, **kwargs):
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None))
        self.config(bg=kwargs.get("bg", None))
        self.title_label.config(bg=kwargs.get("bg", None), fg=kwargs.get("tc", None))
            

class AddAccountPage(Frame):
    def __init__(self, file, website, master, **kwargs):
        super().__init__(master, kwargs)
        self.master = master
        self.file = file
        self.website = website
        self.packed_frames = []
        self.pack_all()


    def title_part(self):
        self.title_frame = Frame(self)
        self.title_label = Label(self.title_frame, text="Add\nAccount", font=("COPPERPLATE GOTHIC BOLD", 30))
        self.title_label.pack(pady=(20, 20))
        self.title_frame.pack()
        self.packed_frames.append(self.title_frame)

    def add_account_page(self):
        add_acc_web_frame = Frame(self)
        # Username entry
        add_username = LabeledEntry(add_acc_web_frame, "Username", font=("Arial", 12), width=18)
        add_username.pack(pady=(0, 10), side="top")

        # Password entry
        add_password = LabeledEntry(add_acc_web_frame, "Password", font=("Arial", 12), width=18)
        add_password.pack(pady=(0, 10))

        generate_pass = Button(add_acc_web_frame,
                            text="Generate password",
                            command=lambda a=add_password: self.gen_pass(a))
        generate_pass.pack(pady=(0, 10))

        save_button = Button(add_acc_web_frame,
                            text="Submit account",
                            command=lambda wn=self.website, au=add_username, ap=add_password: self.save_account(wn, au, ap))
        save_button.pack(pady=(0, 10), side="right")

        back_button = Button(add_acc_web_frame,
                             text="Back",
                             command=self.back)
        back_button.pack(pady=(0,10), side="left")
        self.packed_frames.append(add_acc_web_frame)
        add_acc_web_frame.pack()

    def save_account(self, website_name, add_username, add_password):
        new_pass = add_password.get()
        new_name = add_username.get()
        add_account(self.file, self.password, website_name, new_name, new_pass)

        self.back()

    def gen_pass(self, add_password):
        length = random.randint(9,13)
        self.generated_pass = generate_password(length)
        add_password.delete(0, END)
        add_password.insert(0, self.generated_pass)
        add_password.config(fg="black")

    def back(self):
        self.forget_all()
        self.master.pack_all()

    def forget_all(self):
        for frame in self.packed_frames:
            frame.pack_forget()
        self.pack_forget()

    def pack_all(self):
        self.title_part()
        self.add_account_page()
        self.pack()
        self.color(bg="#1d1e21", tc="#0abf98")

    def color(self, **kwargs):
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None))
        self.config(bg=kwargs.get("bg", None))
        self.title_label.config(bg=kwargs.get("bg", None), fg=kwargs.get("tc", None))

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x400")
    root.config(bg="#1d1e21")

    # login_page = LoginPage(root)
    # login_page.pack_all()
    # login_page.color(bg="#1d1e21", tc="#0abf98")
    file = SaveFile("Rei")
    home = HomePage(file, "hello", root)
    home.page_logic()
    home.pack_all()

    root.mainloop()