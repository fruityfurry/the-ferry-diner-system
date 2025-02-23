import tkinter as tk
from tkinter import messagebox
import pickle
from typing import List, Tuple
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
from OrderDB import OrderDB
from Meal import Meal
from EmployeeDB import EmployeeDB

class ReservationViewer(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Reservation Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.reservationDB = ReservationDB()
        self.reservations = self.reservationDB.reservations
        self.reservations = sorted(self.reservations, key=lambda x: x.time)
        
        self.sortBy = tk.StringVar(self, "Time")
        self.sortBy.trace_add("write", self.sortByChanged)
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        self.numSelectedLabel = widgets.Label(self, text="0 Selected", width=10, height=1)
        self.numSelectedLabel.place(x=400, y=25, anchor="n")
        
        sortByLabel = widgets.Label(self, text="Sort by ", width=9, height=1)
        sortByLabel.place(x=480, y=25)
        sortByDropdown = widgets.Dropdown(self, self.sortBy, *["Time", "Name", "People"])
        sortByDropdown.config(width=12)
        sortByDropdown.place(x=780, y=20, anchor="ne")
        
        self.listbox = widgets.Listbox(self, width=63, height=18)
        self.listbox.bind("<<ListboxSelect>>", self.updateNumSelected)
        self.listbox.place(x=20, y=80)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=14, height=1, command=self.deleteSelected)
        deleteButton.place(x=20, y=580, anchor="sw")
        
        viewMealsButton = widgets.Button(self, text="View Ordered Meals", width=20, height=1, command=self.viewOrderedMeals)
        viewMealsButton.place(x=400, y=580, anchor="s")
        
        self.searchButton = widgets.Button(self, text="Search...", width=14, height=1, command=self.searchDialog)
        self.searchButton.place(x=780, y=580, anchor="se")
        
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        self.updateListbox()
        
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
            
    def updateNumSelected(self, event: tk.Event | None) -> None:
        self.numSelectedLabel.config(text=f"{len(self.listbox.curselection())} Selected")
            
    def sortByChanged(self, varName: str, index: str, action: str) -> None:
        self.sort()
    
    def sort(self) -> None:
        if self.sortBy.get() == "Time":
            self.reservations = sorted(self.reservations, key=lambda x: x.time)
        elif self.sortBy.get() == "Name":
            customers = CustomerDB()
            
            def sortFunc(x: Reservation) -> str:
                customer = customers.getByID(x.customerID)
                return f"{customer.fName} {customer.sName}"
            
            self.reservations = sorted(self.reservations, key=sortFunc)
        elif self.sortBy.get() == "People":
            self.reservations = sorted(self.reservations, key=lambda x: x.peopleNum)
            
        self.updateListbox()
        self.updateNumSelected(None)
    
            
    def updateListbox(self) -> None:
        lines = []
        customers = CustomerDB()
        employees = EmployeeDB()
        
        for reservation in self.reservations:
            customer = customers.getByID(reservation.customerID)
            name = f"{customer.fName} {customer.sName}"
            lines.append(f"{reservation.time} - {name} - {reservation.peopleNum} ppl."
                         f" - Taken by {employees.getByUsername(reservation.employeeUser).name}")
            
        self.listbox.delete(0, tk.END)
        self.listbox.insert(0, *lines)
        
    def getSelected(self) -> List[Reservation]:
        indices: Tuple[int] = self.listbox.curselection()
        
        return [self.reservations[index] for index in indices]
            
    def deleteSelected(self) -> None:
        selected = self.getSelected()
        
        if len(selected) > 0 and messagebox.askyesno("Are you sure?",
                                                     f"Are you sure you want to delete {len(selected)} reservations?"):
            for reservation in selected:
                self.reservationDB.delete(reservation.reservationID)
                self.reservations.remove(reservation)
                
            self.updateListbox()
            self.updateNumSelected(None)
        
    def makeSearch(self, search: ReservationSearch = ReservationSearch()) -> None:
        self.reservations = self.reservationDB.findMatches(search)
        self.sort()
        
    def searchDialog(self) -> None:
        self.searchButton.config(state=tk.DISABLED)
        
        dialog = tk.Toplevel()
        dialog.focus()
        dialog.title("Search Reservations")
        dialog.geometry("800x600")
        dialog.config(bg=colors.BACKGROUND)
        
        timeslots: List[str] = pickle.load(open("data/timeslots.dat", "rb"))
        timeslots = [""] + timeslots
        
        customerName = tk.StringVar(dialog)
        employeeName = tk.StringVar(dialog)
        time = tk.StringVar(dialog)
        time.set(timeslots[0])
        peopleNum = tk.StringVar(dialog)
        
        def resetSearchButton() -> None:
            searchButton.config(fg=colors.FOREGROUND, text="Search")
        
        def error(text: str) -> None:
            searchButton.config(fg=colors.ERROR, text=text)
            dialog.after(1000, resetSearchButton)
        
        def tryMakeSearch() -> None:
            if customerName.get() == "":
                customerSearch = None
            else:
                customerSearch = customerName.get().strip()
                
            if employeeName.get() == "":
                employeeSearch = None
            else:
                employeeSearch = employeeName.get().strip()
                
            if time.get() == "":
                timeSearch = None
            else:
                timeSearch = time.get().strip()
                
            if peopleNum.get() == "":
                peopleNumSearch = None
            else:
                try:
                    peopleNumSearch = int(peopleNum.get().strip())
                    if peopleNumSearch < 1 or peopleNumSearch > 9: raise Exception()
                except:
                    error("Invalid no. of People")
                    return
            
            search = ReservationSearch(time=timeSearch, peopleNum=peopleNumSearch,
                                       customerSearch=customerSearch, employeeSearch=employeeSearch)
            
            dialog.destroy()
            self.searchButton.config(state=tk.NORMAL)
            self.makeSearch(search)
            
        def close() -> None:
            self.searchButton.config(state=tk.NORMAL)
            dialog.destroy()
                            
        customerNameLabel = widgets.Label(dialog, text="Customer Name", width=13)
        customerNameLabel.place(x=275, y=40, anchor="ne")
        customerNameEntry = widgets.Entry(dialog, textvariable=customerName, width=20)
        customerNameEntry.place(x=280, y=40)
        
        employeeNameLabel = widgets.Label(dialog, text="Employee Name", width=13)
        employeeNameLabel.place(x=275, y=160, anchor="ne")
        employeeNameEntry = widgets.Entry(dialog, textvariable=employeeName, width=20)
        employeeNameEntry.place(x=280, y=160)
        
        timeLabel = widgets.Label(dialog, text="Time", width=5)
        timeLabel.place(x=275, y=280, anchor="ne")
        timeDropdown = widgets.Dropdown(dialog, time, *timeslots)
        timeDropdown.config(width=17)
        timeDropdown.place(x=280, y=280)
        
        peopleNumLabel = widgets.Label(dialog, text="No. of People", width=13)
        peopleNumLabel.place(x=275, y=400, anchor="ne")
        peopleNumEntry = widgets.Entry(dialog, textvariable=peopleNum, width=20)
        peopleNumEntry.place(x=280, y=400)
        
        searchButton = widgets.Button(dialog, text="Search", width=20, height=2, command=tryMakeSearch)
        searchButton.place(x=280, y=560, anchor="sw")
        
        cancelButton = widgets.Button(dialog, text="Cancel", width=10, height=1, command=close)
        cancelButton.place(x=40, y=560, anchor="sw")
        
        dialog.protocol("WM_DELETE_WINDOW", close)
        
    def viewOrderedMeals(self) -> None:
        selected = self.getSelected()
        
        customers = CustomerDB()
        orders = OrderDB()
        
        def formatMeals(meals: List[Meal]) -> str:
            text = ""
            mealsSeen = []
            
            for i, meal1 in enumerate(meals):
                if meal1 not in mealsSeen:
                    quantity = 1
                    mealsSeen.append(meal1)
                    
                    for j, meal2 in enumerate(meals):
                        if meal1 == meal2 and i != j:
                            quantity += 1
                        
                    text += f"x{quantity} {meal1.name} - £{round(meal1.price, 2)}\n"
                    
            return text[:-1]  # Exclude last newline character.
        
        for reservation in selected:
            customer = customers.getByID(reservation.customerID)
            meals = orders.getAssociatedMeals(reservation.reservationID)
            messagebox.showinfo(f"{customer.fName} {customer.sName}'s Ordered Meals", formatMeals(meals))