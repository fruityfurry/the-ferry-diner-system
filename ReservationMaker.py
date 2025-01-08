import tkinter as tk
import pickle
from hashing import hash
from typing import List, Dict
from Employee import Employee
import colors
import widgets
from Meal import Meal
from helpers import levenstein
import Login

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
        self.mealNames = [meal.name for meal in self.meals]
        self.time  = tk.StringVar()
        
        self.selectedMeal = self.meals[0].name
        
        fNameLabel = widgets.Label(self, text="First Name", width=10, height=1)
        fNameLabel.place(x=160, y=78, anchor="ne")
        fNameEntry = widgets.Entry(self, textvariable=self.fName, width=20)
        fNameEntry.place(x=160, y=78)
        
        sNameLabel = widgets.Label(self, text="Surname", width=8, height=1)
        sNameLabel.place(x=160, y=160, anchor="ne")
        sNameEntry = widgets.Entry(self, textvariable=self.sName, width=20)
        sNameEntry.place(x=160, y=160)
        
        phoneLabel = widgets.Label(self, text="Phone", width=6, height=1)
        phoneLabel.place(x=160, y=240, anchor="ne")
        phoneEntry = widgets.Entry(self, textvariable=self.phone, width=20)
        phoneEntry.place(x=160, y=240)
        
        self.mealDropdown = widgets.Dropdown(self, self.selectedMeal, *self.mealNames)
        
        self.peopleNum = widgets.Spinbox(self, from_=1, to=9, width=5)
        self.peopleNum.place(x=580, y=460)
        
        self.timeout = self.after(3 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel(self.timeout)
        self.timeout = self.after(3 * 60 * 1000, self.logOut)
        
    def logOut(self) -> None:
        self.destroy()
        Login.Login()
        
    def nameChange(self, varName: str, index: str, action: str) -> None:
        print(self.fName.get())
        print(self.sName.get())