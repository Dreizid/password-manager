from .base_frame import BaseFrame
from .fancy_tkinter import LabeledEntry, Frame, Button, Label
from src.save import SaveFile
from project import *

class LoginPage(BaseFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.TOGGLE_PASSWORD = False
        self.REGISTERED_WARNING = False
        self.CREDENTIAL_WARNING = False
        self.WARNING_PART = False

        # Design constants
        self.background_color = "#1d1e21"
        self.text_color = "#0abf98"
        self.packed_frames.append(self)
        TITLE_PADDING = (20, 20)
        BUTTON_PADY = (10, 10)
        BUTTON_WIDTH = 9

        # Buttons
        REGISTER_BUTTON = {"text": "Register", "command": self.register, "buttonside": "left", "buttonpadx": (0, 20), "buttonpady": BUTTON_PADY}
        LOGIN_BUTTON = {"text": "Login", "command": self.login_event, "buttonside": "right", "buttonpady": BUTTON_PADY}

        # Page initialization
        self.title_part(f"Password\nManager", font=("COPPERPLATE GOTHIC BOLD", 30), textpady=TITLE_PADDING)
        self.entry_part()
        self.button_part(REGISTER_BUTTON, LOGIN_BUTTON, width=BUTTON_WIDTH)
        self.color(bg=self.background_color, fg=self.text_color)

    def entry_part(self):
        ENTRY_FONT = ("Arial", 12)
        BUTTON_FONT = ("Arial", 7)
        BUTTON_WIDTH = 6
        WIDTH = 18
        PADY = (10, 5)
        entry_frame = Frame(self)
        self.username_entry = LabeledEntry(placeholder="Username", master=entry_frame, font=ENTRY_FONT, width=WIDTH)
        self.password_entry = LabeledEntry(placeholder="Password", master=entry_frame, font=ENTRY_FONT, width=13, show="*")
        self.show_button = Button(entry_frame, text="show", command=self.toggle_password, font=BUTTON_FONT, width=BUTTON_WIDTH)
        self.hide_button = Button(entry_frame, text="hide", command=self.toggle_password, font=BUTTON_FONT, width=BUTTON_WIDTH)

        self.username_entry.pack(pady=PADY, side="top")
        self.password_entry.pack(pady=PADY, side="left")
        self.show_button.pack(pady=PADY, side="right")
        entry_frame.pack()
        self.packed_frames.append(entry_frame)

    def warning_part(self, warning_message):
        PADY = (10, 10)
        if self.WARNING_PART:
            self.warning_frame.pack_forget() 
        self.WARNING_PART = True
        self.warning_frame = Frame(self, bg=self.background_color)
        warning_text = Label(self.warning_frame, text=warning_message, bg=self.background_color, fg=self.text_color)
        warning_text.pack(pady=PADY, side="top")
        self.warning_frame.pack()
        self.packed_frames.append(self.warning_frame)

    def login_event(self):
        self.login_username = self.username_entry.get()
        self.login_password = self.password_entry.get()
        self.file = SaveFile(self.login_username)
        user_file_paths = self.file.load_user_config()
        for user_path in user_file_paths["Users"]:
            if self.login_username in user_path["Username"]:
                self.authenticate_credentials()
                return
        if not self.REGISTERED_WARNING:
            self.warning_part(f"User is not registered!")
            self.REGISTERED_WARNING = True

    def authenticate_credentials(self):
        if validate_password(self.file, self.login_password):
            self.login_success()
        else:
            self.warning_part(f"Invalid username or password")
            self.CREDENTIAL_WARNING_WARNING = True

    def login_success(self):
        self.forget_all()
        home_page = HomePage(self.master, file=self.file, username=self.login_username, password=self.login_password)
        # TO DO: Add more?

    def register(self):
        self.forget_all()
        registration_page = RegistrationPage(self)

    def toggle_password(self):
        PADY = (10, 5)
        if self.password_toggle_check():
            self.password_entry.config(show="")
            self.show_button.pack_forget()
            self.hide_button.pack(pady=PADY, side="right")
            self.TOGGLE_PASSWORD = True
        else:
            self.password_entry.config(show="*")
            self.hide_button.pack_forget()
            self.show_button.pack(pady=PADY, side="right")
            self.TOGGLE_PASSWORD = False

    def password_toggle_check(self):
        current_password_entry = self.password_entry.get()
        if not self.TOGGLE_PASSWORD:
            return True 
        elif self.TOGGLE_PASSWORD and current_password_entry != self.password_entry.placeholder and not current_password_entry != "":
            return False
