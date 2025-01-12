import tkinter as tk
import pickle
from typing import List
from Employee import Employee
import colors
import widgets
import Login
from Reservation import Reservation
import AdminMenu
import EmployeeMenu
from ReservationSearch import ReservationSearch
from ReservationDB import ReservationDB
from CustomerDB import CustomerDB

class ReservationViewer(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Reservation Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        reservationDB = ReservationDB()
        self.reservations = reservationDB.reservations
        self.reservations = sorted(self.reservations, key=lambda x: x.time)
        
        self.sortBy = tk.StringVar(self, "Time")
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        self.numSelectedLabel = widgets.Label(self, text="0 Selected", width=10, height=1)
        self.numSelectedLabel.place(x=400, y=25, anchor="n")
        
        sortByLabel = widgets.Label(self, text="Sort by: ", width=9, height=1)
        sortByLabel.place(x=480, y=25)
        sortByDropdown = widgets.Dropdown(self, self.sortBy, *["Time", "Name", "People"])
        sortByDropdown.config(width=12)
        sortByDropdown.place(x=780, y=20, anchor="ne")
        
        self.listbox = widgets.Listbox(self, width=63, height=18)
        self.listbox.place(x=20, y=80)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=14, height=1, command=self.deleteSelected)
        deleteButton.place(x=20, y=580, anchor="sw")
        
        viewMealsButton = widgets.Button(self, text="View Ordered Meals", width=20, height=1, command=self.viewOrderedMeals)
        viewMealsButton.place(x=400, y=580, anchor="s")
        
        searchButton = widgets.Button(self, text="Search...", width=14, height=1, command=self.searchDialog)
        searchButton.place(x=780, y=580, anchor="se")
        
        self.timeout = self.after(3 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        self.updateListbox()
        
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
    
    def makeSearch(self) -> None:
        print("heyo")
            
    def updateListbox(self) -> None:
        lines = []
        customers = CustomerDB()
        
        for reservation in self.reservations:
            customer = customers.getByID(reservation.customerID)
            name = f"{customer.fName} {customer.sName}"
            lines.append(f"{reservation.time} - {name} - {reservation.peopleNum} ppl.")
            
        self.listbox.delete(0, tk.END)
        self.listbox.insert(0, *lines)
        
    def getSelected(self) -> None:
        indexes = self.listbox.curselection()
        print(indexes)
            
    def deleteSelected(self) -> None:
        self.getSelected()
        
    def searchDialog(self) -> None:
        dialog = tk.Toplevel()
        dialog.geometry("800x600")
        dialog.config(bg=colors.BACKGROUND)
        
        
        
    def viewOrderedMeals(self) -> None:
        ...