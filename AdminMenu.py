import tkinter as tk
import pickle
from Employee import Employee
import colors
import widgets

class AdminMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        logOutButton = widgets.Button(self, text="Log Out", width=10, height=2)
        logOutButton.place(x=18, y=18)
        
        self.mainloop()