from tkinter import Frame, Label, Button

class BaseFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.file = kwargs.get("file", None)
        self.login_username = kwargs.get("username", None)
        self.login_password = kwargs.get("password", None)
        self.packed_frames = [self]

    def title_part(self, title, **kwargs):
        title_frame = Frame(self)
        self.title_text = Label(title_frame, text=title, font=kwargs.get("font", None))
        title_frame.pack(pady=kwargs.get("framepady", None), padx=kwargs.get("framepadx", None), side=kwargs.get("frameside", None))
        self.title_text.pack(pady=kwargs.get("textpady", None), padx=kwargs.get("textpadx", None), side=kwargs.get("textside", None))
        self.packed_frames.append(title_frame)

    def button_part(self, *args, **kwargs):
        button_frame = Frame(self)
        for arg in args:
            self.button = Button(button_frame, text=arg.get("text", None), command=arg.get("command", None), **kwargs)
            button_frame.pack(pady=arg.get("framepady", None), padx=arg.get("framepaxy", None), side=arg.get("frameside", None))
            self.button.pack(pady=arg.get("buttonpady", None), padx=arg.get("buttonpadx", None), side=arg.get("buttonside", None))
            self.packed_frames.append(button_frame)

    def pack_all(self):
        self.pack(fill="both", expand="true")
        for frame in self.packed_frames:
            frame.pack()

    def forget_all(self):
        for frame in self.packed_frames:
            frame.pack_forget()

    def previous_page(self):
        self.forget_all()
        self.master.pack_all()

    def color(self, **kwargs):
        for frame in self.packed_frames:
            frame.config(bg=kwargs.get("bg", None))
        self.title_text.config(bg=kwargs.get("bg", None), fg=kwargs.get("fg", None))


    
