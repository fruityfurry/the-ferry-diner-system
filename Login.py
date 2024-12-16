import tkinter as tk
from tkinter import ttk
from hashlib import sha256 as hash
import colors
import styles

class Login(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.config(bg=colors.BACKGROUND)
        
        styles.defineAllStyles(self)
        
        self.user = tk.StringVar();
        
        logoImg = tk.PhotoImage(file="resources/diner.png")
        logo = ttk.Label(self, image=logoImg)
        logo.place(x=240, y=80)
        
        userEntry = ttk.Entry(self, textvariable=self.user, style="TEntry")
        userEntry.place(x=280, y=300)
        
        self.mainloop()