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

class AccountLabels(Label):
    def __init__(self, index, account, root, file, website, master, **kwargs):
        super().__init__(master, **kwargs)
        self.index = index
        self.account = account
        self.root = root
        self.file = file
        self.website = website
        self.packed_frames = []
        self.labels()
        self.popup_menu()
        self.binding()

    def labels(self):
        text_width = 0
        text_color = "white"
        account_no = Label(self, text=f"Account {self.index + 1}", font=("Arial", 10), anchor="w", fg=text_color)
        account_no.pack()

        # Username label
        username_label = ClipboardLabel(self,
                                        text=f"Username: {self.account['Username']}", data=self.account['Username'],
                                        anchor="w",
                                        width=text_width,
                                        font=("Arial", 12),
                                        fg=text_color)
        username_label.pack()

        # Password label
        password_label = ClipboardLabel(self,
                                        text=f"Password: {self.account['Password']}", data=self.account['Password'],
                                        anchor="w",
                                        width=text_width,
                                        font=("Arial", 12),
                                        fg=text_color)
        password_label.pack()

        self.packed_frames.append(account_no)
        self.packed_frames.append(username_label)
        self.packed_frames.append(password_label)

    def binding(self):
        for frame in self.packed_frames:
            frame.bind("<Button-3>", self.do_popup)

    def do_popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def popup_menu(self):
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Edit", command=self.edit_entry)
        self.menu.add_command(label="Remove", command=self.remove)


    def edit_entry(self):
        self.master.call_edit()

    def remove(self):
        self.file.remove(self.website, self.index)

    def color(self, **kwargs):
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None), fg=kwargs.get("tc", None))
        self.config(bg=kwargs.get("bg", None))