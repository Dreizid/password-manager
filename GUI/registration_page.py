from .base_frame import BaseFrame
from .fancy_tkinter import LabeledEntry
from tkinter import Frame

class RegistrationPage(BaseFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def entry_part(self):
        FONT = ("Arrial", 12)
        WIDTH = 18
        entry_frame = Frame(self)
        username_entry = LabeledEntry(placeholder="Username", master=self, font=FONT, width=WIDTH)
        password_entry = LabeledEntry(placeholder="Password", master=self, font=FONT, width=WIDTH)
        confirm_password_entry = LabeledEntry(placeholder="Confirm Password", master=self, font=FONT, width=WIDTH)

    def warning_part(self):
        pass

    def register_event(self):
        pass