from tkinter import Tk
from GUI.login_page import LoginPage
from src.save import SaveFile

root = Tk()
root.geometry("300x400")

login_page = LoginPage(root)
login_page.pack_all()
root.mainloop()