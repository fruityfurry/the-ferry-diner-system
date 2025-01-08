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
        self.fName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.sName = tk.StringVar()
        self.sName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.phone = tk.StringVar()
        self.meals: List[Meal] = pickle.load(open("data/meals.dat", "rb"))
        self.mealNames = [meal.name for meal in self.meals]
        self.time  = tk.StringVar()
        
        self.selectedMeal = tk.StringVar()
        self.selectedMeal.set(self.meals[0].name)
        
        self.customerSearchText = tk.StringVar()
        self.customerSearchText.set("Start typing to search customers.")
        
        self.similarCustomer = None
        
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
        
        mealLabel = widgets.Label(self, text="Meal", width=5, height=1)
        mealLabel.place(x=160, y=320, anchor="ne")
        mealDropdown = widgets.Dropdown(self, self.selectedMeal, *self.mealNames)
        mealDropdown.place(x=160, y=320)
        
        removeButton = widgets.Button(self, text="Remove", width=9, height=1, command=self.removeMeal)
        removeButton.place(x=160, y=380)
        
        addButton = widgets.Button(self, text="Add", width=9, height=1, command=self.addMeal)
        addButton.place(x=293, y=380)
        
        timeLabel = widgets.Label(self, text="Time", width=5, height=1)
        timeLabel.place(x=160, y=460, anchor="ne")
        timeEntry = widgets.Entry(self, textvariable=self.phone, width=20)
        timeEntry.place(x=160, y=460)
        
        customerSearch = widgets.Label(self, textvariable=self.customerSearchText, width=25, height=4, wraplength=280)
        customerSearch.config(bg=colors.ITEM, highlightbackground=colors.OUTLINE, highlightthickness=2,)
        customerSearch.place(x=458, y=60)
        
        autofillButton = widgets.Button(self, text="Autofill Details", width=16, height=1, command=self.autofill)
        autofillButton.place(x=508, y=180)
        
        mealsAddedTextBox = widgets.TextBox(self, width=25, height=5)
        mealsAddedTextBox.setText("No meals added yet.")
        mealsAddedTextBox.place(x=458, y=240)
        
        totalPriceLabel = widgets.Label(self, text="Total: £0.00", width=25, height=1, anchor="w")
        totalPriceLabel.place(x=458, y=387)
        
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
        
    def addMeal(self) -> None:
        ...
        
    def removeMeal(self) -> None:
        ...
        
    def autofill(self) -> None:
        ...