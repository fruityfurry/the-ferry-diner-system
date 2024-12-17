import tkinter as tk
from Employee import Employee
import colors
import widgets

class ReservationMaker(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.peopleNum = widgets.Spinbox(self, from_=1, to=9, width=5)
        self.peopleNum.place(x=580, y=460)
        