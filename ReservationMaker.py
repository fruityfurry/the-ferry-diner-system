import tkinter as tk
from Employee import Employee
from typing import List
from Meal import Meal
from helpers import levenstein
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
        
        self.fName = tk.StringVar()
        self.fName.trace_add("write", self.nameChange)
        self.sName = tk.StringVar()
        self.sName.trace_add("write", self.nameChange)
        self.phone = tk.StringVar()
        self.meals: List[Meal] = []
        self.time  = tk.StringVar()
        
        fNameEntry = widgets.Entry(self, textvariable=self.fName, width=20)
        fNameEntry.place(x=20, y=20)
        
        sNameEntry = widgets.Entry(self, textvariable=self.sName, width=20)
        sNameEntry.place(x=20, y=120)
        
        self.peopleNum = widgets.Spinbox(self, from_=1, to=9, width=5)
        self.peopleNum.place(x=580, y=460)
        
    def nameChange(self, varName: str, index: str, action: str) -> None:
        print(self.fName.get())
        print(self.sName.get())