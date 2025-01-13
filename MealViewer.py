import tkinter as tk
from typing import List, Tuple
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
import EmployeeMenu
from MealDB import MealDB
from Meal import Meal
from MealSearch import MealSearch

class MealViewer(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Reservation Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.mealDB = MealDB()
        self.meals = self.mealDB.meals
        self.meals = sorted(self.meals, key=lambda x: x.name)
        
        self.sortBy = tk.StringVar(self, "Name")
        self.sortBy.trace_add("write", self.sortByChanged)
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        self.numSelectedLabel = widgets.Label(self, text="0 Selected", width=10, height=1)
        self.numSelectedLabel.place(x=400, y=25, anchor="n")
        
        sortByLabel = widgets.Label(self, text="Sort by ", width=9, height=1)
        sortByLabel.place(x=480, y=25)
        sortByDropdown = widgets.Dropdown(self, self.sortBy, *["Name", "Price"])
        sortByDropdown.config(width=12)
        sortByDropdown.place(x=780, y=20, anchor="ne")
        
        self.listbox = widgets.Listbox(self, width=63, height=18)
        self.listbox.bind("<<ListboxSelect>>", self.updateNumSelected)
        self.listbox.place(x=20, y=80)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=14, height=1, command=self.deleteSelected)
        deleteButton.place(x=20, y=580, anchor="sw")
        
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
            
    def updateNumSelected(self, event: tk.Event | None) -> None:
        self.numSelectedLabel.config(text=f"{len(self.listbox.curselection())} Selected")
            
    def sortByChanged(self, varName: str, index: str, action: str) -> None:
        self.sort()
    
    def sort(self) -> None:
        if self.sortBy.get() == "Name":
            self.meals = sorted(self.meals, key=lambda x: x.name)
        elif self.sortBy.get() == "Price":
            self.meals = sorted(self.meals, key=lambda x: x.price)
            
        self.updateListbox()
        self.updateNumSelected(None)
    
            
    def updateListbox(self) -> None:
        lines = []
        
        for meal in self.meals:
            lines.append(f"{meal.name} - £{meal.price}")
            
        self.listbox.delete(0, tk.END)
        self.listbox.insert(0, *lines)
        
    def getSelected(self) -> List[Meal]:
        indexes: Tuple[int] = self.listbox.curselection()
        
        return [self.meals[index] for index in indexes]
            
    def deleteSelected(self) -> None:
        selected = self.getSelected()
        
        for reservation in selected:
            self.mealDB.delete(reservation.mealID)
            self.meals.remove(reservation)
            
        self.updateListbox()
        self.updateNumSelected(None)
        
    def makeSearch(self, search: MealSearch = MealSearch()) -> None:
        self.meals = self.mealDB.findMatches(search)
        self.sort()
        
    def searchDialog(self) -> None:
        dialog = tk.Toplevel()
        dialog.title("Search Reservations")
        dialog.geometry("800x600")
        dialog.config(bg=colors.BACKGROUND)
        
        name = tk.StringVar(dialog)
        price = tk.StringVar(dialog)
        
        def resetSearchButton() -> None:
            
            searchButton.config(fg=colors.FOREGROUND, text="Search")
        
        def error(text: str) -> None:
            searchButton.config(fg=colors.ERROR, text=text)
            dialog.after(1000, resetSearchButton)
        
        def tryMakeSearch() -> None:
            if name.get() == "":
                nameSearch = None
            else:
                nameSearch = name.get()
                
            if price.get() == "":
                priceSearch = None
            else:
                try:
                    priceSearch = float(price.get())
                except:
                    error("Invalid Price")
                    return
            
            search = MealSearch(nameSearch, priceSearch)
            
            dialog.destroy()
            self.makeSearch(search)
                            
        customerNameLabel = widgets.Label(dialog, text="Name", width=5)
        customerNameLabel.place(x=275, y=200, anchor="ne")
        customerNameEntry = widgets.Entry(dialog, textvariable=name, width=20)
        customerNameEntry.place(x=280, y=200)
        
        peopleNumLabel = widgets.Label(dialog, text="Price", width=6)
        peopleNumLabel.place(x=275, y=300, anchor="ne")
        peopleNumEntry = widgets.Entry(dialog, textvariable=price, width=20)
        peopleNumEntry.place(x=280, y=300)
        
        searchButton = widgets.Button(dialog, text="Search", width=20, height=2, command=tryMakeSearch)
        searchButton.place(x=280, y=560, anchor="sw")
        
        cancelButton = widgets.Button(dialog, text="Cancel", width=10, height=1, command=dialog.destroy)
        cancelButton.place(x=40, y=40)