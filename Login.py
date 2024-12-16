import tkinter as tk
from hashlib import sha256 as hash
import colors
import widgets

class Login(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.config(bg=colors.BACKGROUND)
        
        self.user = tk.StringVar();
        
        logoImg = tk.PhotoImage(file="resources/diner.png")
        logo = tk.Label(self, image=logoImg, borderwidth=0)
        logo.place(x=400, y=40, anchor="n")
        
        userEntry = widgets.Entry(self, textvariable=self.user)
        userEntry.place(x=265, y=300)
        
        self.mainloop()