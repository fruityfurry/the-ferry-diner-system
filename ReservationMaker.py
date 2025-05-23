import tkinter as tk
import pickle
from typing import List, Tuple
from Employee import Employee
import colors
import widgets
from Meal import Meal
import Login
import AdminMenu
import EmployeeMenu
from CustomerDB import CustomerDB
from ReservationDB import ReservationDB
from Reservation import Reservation
from MealDB import MealDB
from EmployeeDB import EmployeeDB
from helpers import roundPrice, quicksort

class ReservationMaker(tk.Tk):
    def __init__(self, user: Employee, reservationFill: Reservation | None = None, *args, **kwargs) -> None:
        """Reservation maker window."""
        super().__init__(*args, **kwargs)
        self.title("Reservation Maker")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.customers = CustomerDB()
        
        self.fName = tk.StringVar()
        self.fName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.sName = tk.StringVar()
        self.sName.trace_add("write", self.nameChange)  # Allows tracking when value is changed.

        self.phone = tk.StringVar()
        self.mealsOrdered: List[Tuple[Meal, int]] = []
        self.meals = MealDB()
        
        mealNames = [meal.name for meal in self.meals.meals]  # List of names of meals for meal dropdown.
        quicksort(mealNames)
        timeslots: List[str] = pickle.load(open("data/timeslots.dat", "rb"))  # List of timeslots for time dropdown.
        self.time = tk.StringVar()
        
        self.peopleNum = tk.IntVar()
        
        self.selectedMeal = tk.StringVar()
        self.selectedMeal.set(mealNames[0])
        
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
        mealDropdown.config(width=17)
        mealDropdown.place(x=160, y=320)
        
        clearButton = widgets.Button(self, text="Clear", width=9, height=1, command=self.clearMeals)
        clearButton.place(x=780, y=380, anchor="ne")
        
        removeButton = widgets.Button(self, text="Remove", width=9, height=1, command=self.removeMeal)
        removeButton.place(x=160, y=380)
        
        addButton = widgets.Button(self, text="Add", width=9, height=1, command=self.addMeal)
        addButton.place(x=293, y=380)
        
        timeLabel = widgets.Label(self, text="Time", width=5, height=1)
        timeLabel.place(x=160, y=460, anchor="ne")
        timeDropdown = widgets.Dropdown(self, self.time, *timeslots)
        timeDropdown.config(width=17)
        timeDropdown.place(x=160, y=460)
        
        customerSearch = widgets.Label(self, textvariable=self.customerSearchText, width=25, height=4, wraplength=280)
        customerSearch.config(bg=colors.ITEM, highlightbackground=colors.OUTLINE, highlightthickness=2,)
        customerSearch.place(x=458, y=60)
        
        self.autofillButton = widgets.Button(self, text="Autofill Details", width=16, height=1, command=self.autofill,
                                             state=tk.DISABLED)
        self.autofillButton.place(x=508, y=180)
        
        self.mealsAddedTextBox = widgets.TextBox(self, width=25, height=5)
        self.mealsAddedTextBox.setText("No meals added yet.")
        self.mealsAddedTextBox.place(x=458, y=240)
        
        self.totalPriceLabel = widgets.Label(self, text="Total: £0.00", width=15, height=1, anchor="w")
        self.totalPriceLabel.place(x=458, y=387)
        
        peopleNumLabel = widgets.Label(self, text="No. of People", width=13, height=1)
        peopleNumLabel.place(x=422, y=460)
        peopleNumSpinbox = widgets.Spinbox(self, from_=1, to=9, width=5, textvariable=self.peopleNum)
        peopleNumSpinbox.place(x=580, y=457)
        
        self.makeReservationButton = widgets.Button(self, text="Make Reservation", width=20, height=2,
                                                    command=self.makeReservation)
        self.makeReservationButton.place(x=400, y=520, anchor="n")
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20, anchor="nw")
        
        if reservationFill is not None:  # A reservation was given, so fill the fields.
            reservationDB = ReservationDB()
            employeeDB = EmployeeDB()
            customerDB = CustomerDB()
            
            customer = customerDB.getByID(reservationFill.customerID)
            meals = reservationDB.getAssociatedMeals(reservationFill.reservationID)
            
            self.fName.set(customer.fName)
            self.sName.set(customer.sName)
            self.phone.set(customer.phone)
            self.mealsOrdered = meals
            self.time.set(reservationFill.time)
            self.peopleNum.set(reservationFill.peopleNum)
            
            employeeDB.decrementReservationsMade(reservationFill.employeeUser)  # Avoid double counting reservation.
            reservationDB.delete(reservationFill.reservationID)  # Delete incorrect reservation.
            
            # Update the similar customer search and meal boxes so they display properly.
            self.nameChange("", "", "")
            self.formatMeals()
            self.updateTotal()
        
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        # Bind return key to press the make reservation button.
        self.bind("<Return>", lambda e: self.makeReservation())  # Lambda to resolve differing arguments.
        
        # Bind escape key to return to menu.
        self.bind("<Escape>", lambda e: self.returnToMenu())  # Lambda to resolve differing arguments.
        
        # Focus on first text entry to ready it for typing immediately.
        # After needed to resolve bug where using .focus() doesn't work.
        self.after(1, lambda: [self.focus_force(), fNameEntry.focus()])
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel(self.timeout)
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        
    def logOut(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        Login.Login()
        
    def returnToMenu(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        if self.user.username == "colinr83":
            AdminMenu.AdminMenu(self.user)
        else:
            EmployeeMenu.EmployeeMenu(self.user)
        
    def error(self, message: str) -> None:
        # Display error message on Make Reservation button and remove after one second.
        self.makeReservationButton.config(text=message, fg=colors.ERROR)
        self.after(1000, self.resetMakeReservationButton)
        
    def resetMakeReservationButton(self) -> None:
        self.makeReservationButton.config(text="Make Reservation", fg=colors.FOREGROUND)
    
    # Called when either name field is changed.
    def nameChange(self, varName: str, index: str, action: str) -> None:
        fullName = self.fName.get().strip() + " " + self.sName.get().strip()
        fullName = fullName.lower()
        
        if fullName == " ":
            self.customerSearchText.set("Start typing to search customers.")
            return
        
        matchesFound = 0
        
        # If match found, suggest they be autofilled.
        for customer in self.customers.customers:
            customerFullName = customer.fName + " " + customer.sName
            customerFullName = customerFullName.lower()
            
            if fullName == customerFullName:
                self.similarCustomer = customer
                self.autofillButton.config(state=tk.NORMAL)
                self.customerSearchText.set(
                    fullName.title() +
                    f" found!{'\nHowever, there are other\ncustomers with the same name.' if matchesFound > 0 else ''}"
                    )
                matchesFound += 1
            elif matchesFound == 0:
                self.similarCustomer = None
                self.autofillButton.config(state=tk.DISABLED)
                self.customerSearchText.set("No match found for " + fullName.title())
             
    # Takes list of meals ordered and formats them into a nice format with quantities and such   
    def formatMeals(self) -> None:
        text = ""
        
        for mealAndQuantity in self.mealsOrdered:
            text += f"x{mealAndQuantity[1]} {mealAndQuantity[0].name} - £{roundPrice(mealAndQuantity[0].price)}\n"
            
        self.mealsAddedTextBox.setText(text[:-1])  # Exclude last newline character.
                
    # Update total text with correct total of meals ordered.
    def updateTotal(self) -> None:
        total = 0
        
        for mealAndQuantity in self.mealsOrdered:
            total += mealAndQuantity[0].price * mealAndQuantity[1]  # Add meal price multiplied by quantity of that meal.
            
        self.totalPriceLabel.config(text=f"Total: £{roundPrice(total)}")
        
    def clearMeals(self) -> None:
        self.mealsOrdered = []
        self.mealsAddedTextBox.setText("No meals added yet.")
        self.updateTotal()
    
    # Add meal to list of ordered meals and update meal box and total.
    def addMeal(self) -> None:
        selectedMeal = self.meals.getByName(self.selectedMeal.get())
        
        for i, mealAndQuantity in enumerate(self.mealsOrdered):
            if mealAndQuantity[0] == selectedMeal:
                self.mealsOrdered[i] = (mealAndQuantity[0], mealAndQuantity[1] + 1)
                self.formatMeals()
                self.updateTotal()
                return
            
        # If the code made it through the whole for loop, this meal must not be in the list.
        self.mealsOrdered.append((selectedMeal, 1))
        
        self.formatMeals()
        self.updateTotal()
        
    # Remove meal from list of ordered meals and update meal box and total.
    def removeMeal(self) -> None:
        selectedMeal = self.meals.getByName(self.selectedMeal.get())
        
        for i, mealAndQuantity in enumerate(self.mealsOrdered):
            if mealAndQuantity[0] == selectedMeal:
                if mealAndQuantity[1] == 1:
                    self.mealsOrdered.remove(mealAndQuantity)
                else:
                    self.mealsOrdered[i] = (mealAndQuantity[0], mealAndQuantity[1] - 1)
                    
                break
        
        if len(self.mealsOrdered) == 0:
            self.mealsAddedTextBox.setText("No meals added yet.")
        else:
            self.formatMeals()
            
        self.updateTotal()
    
    # Fill in customer details with similar customer details, if there is one.
    def autofill(self) -> None:
        if self.similarCustomer is not None:
            self.fName.set(self.similarCustomer.fName)
            self.sName.set(self.similarCustomer.sName)
            self.phone.set(self.similarCustomer.phone)
        
    def makeReservation(self) -> None:
        # Strip fields and properly capitalise them.
        fName = self.fName.get().strip().title()
        sName = self.sName.get().strip().title()
        phone = self.phone.get().strip()
        
        if fName == "":
            self.error("First name empty")
        elif len(fName) > 20:
            self.error("First name too long")
        elif not fName.isalpha():
            self.error("First name invalid")
        elif self.sName == "":
            self.error("Surname empty")
        elif len(sName) > 20:
            self.error("Surname too long")
        elif not sName.isalpha():
            self.error("Surname invalid")
        elif len(phone) != 11:
            self.error("Invalid phone number length")
        elif not phone.isnumeric():
            self.error("Invalid phone number")
        elif len(self.mealsOrdered) == 0:
            self.error("Meals empty")
        elif self.time.get() == "":
            self.error("Time empty")
        else:
            reservations = ReservationDB()
            time = self.time.get()
            peopleNum = self.peopleNum.get()
            
            # Check if customer already exists.
            customerFound = self.customers.exists(fName, sName, phone)
            
            if not customerFound:  # If none found, make a new customer and use their customer ID.
                self.customers.add(fName, sName, phone)
                customerID = self.customers.customers[-1].customerID
            else:  # If found, use their customer ID.
                customerID = self.customers.getID(fName, sName, phone)
            
            # Place reservation.
            reservations.add(customerID, self.user.username, time, peopleNum, self.mealsOrdered)
            
            employees = EmployeeDB()
            employees.incrementReservationsMade(self.user.username)
                
            self.makeReservationButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
            
            self.after(1000, self.returnToMenu)