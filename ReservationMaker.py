import tkinter as tk
import pickle
from typing import List
from Employee import Employee
from Customer import Customer
import colors
import widgets
from Meal import Meal
import Login
from Reservation import Reservation
import AdminMenu
import EmployeeMenu
from CustomerDB import CustomerDB
from ReservationDB import ReservationDB
from MealDB import MealDB
from EmployeeDB import EmployeeDB

class ReservationMaker(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Reservation Maker")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.fName = tk.StringVar()
        self.fName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.sName = tk.StringVar()
        self.sName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.phone = tk.StringVar()
        self.mealsOrdered: List[Meal] = []
        self.customers = CustomerDB()
        self.meals = MealDB()
        mealNames = [meal.name for meal in self.meals.meals]
        timeslots: List[str] = pickle.load(open("data/timeslots.dat", "rb"))
        self.time = tk.StringVar()
        
        self.selectedMeal = tk.StringVar()
        self.selectedMeal.set(self.meals.meals[0].name)
        
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
        mealDropdown = widgets.Dropdown(self, self.selectedMeal, *mealNames)
        mealDropdown.place(x=160, y=320)
        
        removeButton = widgets.Button(self, text="Remove", width=9, height=1, command=self.removeMeal)
        removeButton.place(x=160, y=380)
        
        addButton = widgets.Button(self, text="Add", width=9, height=1, command=self.addMeal)
        addButton.place(x=293, y=380)
        
        timeLabel = widgets.Label(self, text="Time", width=5, height=1)
        timeLabel.place(x=160, y=460, anchor="ne")
        timeEntry = widgets.Dropdown(self, self.time, *timeslots)
        timeEntry.place(x=160, y=460)
        
        customerSearch = widgets.Label(self, textvariable=self.customerSearchText, width=25, height=4, wraplength=280)
        customerSearch.config(bg=colors.ITEM, highlightbackground=colors.OUTLINE, highlightthickness=2,)
        customerSearch.place(x=458, y=60)
        
        self.autofillButton = widgets.Button(self, text="Autofill Details", width=16, height=1, command=self.autofill, state=tk.DISABLED)
        self.autofillButton.place(x=508, y=180)
        
        self.mealsAddedTextBox = widgets.TextBox(self, width=25, height=5)
        self.mealsAddedTextBox.setText("No meals added yet.")
        self.mealsAddedTextBox.place(x=458, y=240)
        
        self.totalPriceLabel = widgets.Label(self, text="Total: £0.00", width=25, height=1, anchor="w")
        self.totalPriceLabel.place(x=458, y=387)
        
        peopleNumLabel = widgets.Label(self, text="No. of People", width=13, height=1)
        peopleNumLabel.place(x=422, y=460)
        self.peopleNum = widgets.Spinbox(self, from_=1, to=9, width=5)
        self.peopleNum.place(x=580, y=457)
        
        self.makeReservationButton = widgets.Button(self, text="Make Reservation", width=20, height=2, command=self.makeReservation)
        self.makeReservationButton.place(x=400, y=520, anchor="n")
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=540)
        
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
        
    def returnToMenu(self) -> None:
        self.destroy()
        if self.user.username == "colinr83":
            AdminMenu.AdminMenu(self.user)
        else:
            EmployeeMenu.EmployeeMenu(self.user)
        
    def error(self, message: str) -> None:
        # Display error message on Make Reservation button and remove after three seconds.
        self.makeReservationButton.config(text=message)
        self.makeReservationButton.config(fg=colors.ERROR)
        self.after(3000, self.resetMakeReservationButton)
        
    def resetMakeReservationButton(self) -> None:
        self.makeReservationButton.config(text="Make Reservation")
        self.makeReservationButton.config(fg=colors.FOREGROUND)
        
    def nameChange(self, varName: str, index: str, action: str) -> None:
        fullName = self.fName.get() + " " + self.sName.get()
        fullName = fullName.lower()
        
        # If match found, suggest they be autofilled.
        for customer in self.customers.customers:
            customerFullName = customer.fName + " " + customer.sName
            customerFullName = customerFullName.lower()
            
            if fullName == customerFullName:
                self.similarCustomer = customer
                self.autofillButton.config(state=tk.NORMAL)
                self.customerSearchText.set(fullName + " found!")
                break
            else:
                self.similarCustomer = None
                self.autofillButton.config(state=tk.DISABLED)
                self.customerSearchText.set("No match found for " + fullName)
                
    def formatMeals(self) -> None:
        text = ""
        mealsSeen = []
        
        for i, meal1 in enumerate(self.mealsOrdered):
            if meal1 not in mealsSeen:
                quantity = 1
                mealsSeen.append(meal1)
                
                for j, meal2 in enumerate(self.mealsOrdered):
                    if meal1 == meal2 and i != j:
                        quantity += 1
                    
                text += f"x{quantity} {meal1.name} - £{round(meal1.price, 2)}\n"
                
        self.mealsAddedTextBox.setText(text[:-1])  # Exclude last newline character.
                
    def updateTotal(self) -> None:
        total = 0
        
        for meal in self.mealsOrdered:
            total += meal.price
            
        self.totalPriceLabel.config(text=f"£{round(total, 2)}")
        
    def addMeal(self) -> None:
        selectedMeal = self.selectedMeal.get()
        
        selectedMeal = self.meals.getByName(selectedMeal)
        
        self.mealsOrdered.append(selectedMeal)
        self.formatMeals()
        self.updateTotal()
        
    def removeMeal(self) -> None:
        selectedMeal = self.selectedMeal.get()
        
        selectedMeal = self.meals.getByName(selectedMeal)
            
        try:
            self.mealsOrdered.remove(selectedMeal)
        except:
            pass
        
        if len(self.mealsOrdered) == 0:
            self.mealsAddedTextBox.setText("No meals added yet.")
        else:
            self.formatMeals()
            
        self.updateTotal()
        
    def autofill(self) -> None:
        if self.similarCustomer is not None:
            self.fName.set(self.similarCustomer.fName)
            self.sName.set(self.similarCustomer.sName)
            self.phone.set(self.similarCustomer.phone)
        
    def makeReservation(self) -> None:
        if self.fName.get() == "":
            self.error("First name empty")
        elif len(self.fName.get()) > 20:
            self.error("First name too long")
        elif self.sName.get() == "":
            self.error("Surname empty")
        elif len(self.sName.get()) > 20:
            self.error("Surname too long")
        elif len(self.phone.get()) != 11:
            self.error("Invalid phone number")
        elif not self.phone.get().isnumeric():
            self.error("Invalid phone number")
        elif len(self.mealsOrdered) == 0:
            self.error("Meals empty")
        elif self.time.get() == "":
            self.error("Time empty")
        else:
            reservations = ReservationDB()
            fName = self.fName.get()
            sName = self.sName.get()
            phone = self.phone.get()
            time  = self.time.get()
            peopleNum = int(self.peopleNum.get())
            
            customerFound = self.customers.exists(fName, sName, phone)
                    
            if not customerFound:
                self.customers.add(fName, sName, phone)
                customerID = self.customers.customers[-1].customerID
            else:
                customerID = self.customers.getID(fName, sName, phone)
                
            reservations.add(customerID, self.user.username, time, peopleNum, self.mealsOrdered)
            
            employees = EmployeeDB()
            employees.incrementReservationsMade(self.user.username)
                    
            with open("data/employees.dat", "wb") as file:
                pickle.dump(employees, file)
                
            self.makeReservationButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
            
            self.after(1 * 1000, self.returnToMenu)