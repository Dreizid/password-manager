from tkinter import *
import pyperclip

class LabeledEntry(Entry):
    def __init__(self, master, placeholder, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.config(fg="gray")
        self.bind("<FocusIn>", self.click_in)
        self.bind("<FocusOut>", self.click_out)

    def click_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self.config(fg="black")

    def click_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg="gray")
    
class ClipboardLabel(Label):
    def __init__(self, master, text, data, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.data = data
        self.bind("<Button-1>", self.copy_to_clipboard)

    def copy_to_clipboard(self, event):
        pyperclip.copy(self.data)
        # Optional: Inform user that text was copied

class ClipboardText(Text):
    def __init__(self, master, text, data, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.data = data
        self.bind("<Button-1>", self.copy_to_clipboard)

    def copy_to_clipboard(self, event):
        pyperclip.copy(self.data)

