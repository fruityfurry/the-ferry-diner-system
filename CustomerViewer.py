import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
from CustomerDB import CustomerDB
from Customer import Customer
from CustomerSearch import CustomerSearch
from helpers import quicksort

class CustomerViewer(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        """Customer viewer window."""
        super().__init__(*args, **kwargs)
        self.title("Customer Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.customerDB = CustomerDB()
        self.customers = [x for x in self.customerDB.customers]  # Avoid passing by reference.
        quicksort(self.customers, lambda x: x.fName)  # Sort list.
        
        self.sortBy = tk.StringVar(self, "First Name")
        self.sortBy.trace_add("write", self.sortByChanged)  # Call function when sort is changed.
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        self.numSelectedLabel = widgets.Label(self, text="0 Selected", width=10, height=1)
        self.numSelectedLabel.place(x=400, y=25, anchor="n")
        
        sortByLabel = widgets.Label(self, text="Sort by ", width=9, height=1)
        sortByLabel.place(x=480, y=25)
        sortByDropdown = widgets.Dropdown(self, self.sortBy, *["First Name", "Surname"])
        sortByDropdown.config(width=12)
        sortByDropdown.place(x=780, y=20, anchor="ne")
        
        self.listbox = widgets.Listbox(self, width=63, height=18)
        self.listbox.bind("<<ListboxSelect>>", self.updateNumSelected)
        self.listbox.place(x=20, y=80)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=14, height=1, command=self.deleteSelected)
        deleteButton.place(x=20, y=580, anchor="sw")
        
        self.searchButton = widgets.Button(self, text="Search...", width=14, height=1, command=self.searchDialog)
        self.searchButton.place(x=780, y=580, anchor="se")
        
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        # Bind escape key to return to menu.
        self.bind("<Escape>", lambda e: self.returnToMenu())  # Lambda to resolve differing arguments.
        
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
        AdminMenu.AdminMenu(self.user)  # This is an admin window so always return to admin menu.
            
    def updateNumSelected(self, event: tk.Event | None) -> None:
        self.numSelectedLabel.config(text=f"{len(self.listbox.curselection())} Selected")
            
    def sortByChanged(self, varName: str, index: str, action: str) -> None:
        self.sort()
    
    def sort(self) -> None:
        # Sort by appropriate attribute depending on selection.
        if self.sortBy.get() == "First Name":
              quicksort(self.customers, lambda x: x.fName)
        elif self.sortBy.get() == "Surname":
              quicksort(self.customers, lambda x: x.sName)
            
        self.updateListbox()
        self.updateNumSelected(None)
    
    def updateListbox(self) -> None:
        """Update the listbox.
        This function must be called whenever the underlying list is changed, otherwise it will not display correctly."""
        lines = []
        
        for customer in self.customers:
            lines.append(f"{customer.fName} {customer.sName} - {customer.phone}")
            
        self.listbox.delete(0, tk.END)
        self.listbox.insert(0, *lines)
        
    def getSelected(self) -> List[Customer]:
        indices: Tuple[int] = self.listbox.curselection()
        
        return [self.customers[index] for index in indices]
            
    def deleteSelected(self) -> None:
        selected = self.getSelected()
        
        if len(selected) > 0 and messagebox.askyesno("Are you sure?",
                                                     f"Are you sure you want to delete {len(selected)} customers?"):
            for customer in selected:
                self.customerDB.delete(customer.customerID)
                self.customers.remove(customer)
                
            self.updateListbox()
            self.updateNumSelected(None)
        
    def makeSearch(self, search: CustomerSearch) -> None:
        self.customers = self.customerDB.findMatches(search)
        self.sort()  # Sort updates listbox itself, so no need to call it.
        
    def searchDialog(self) -> None:
        self.searchButton.config(state=tk.DISABLED)  # Prevent making multiple search dialogs.
        
        dialog = tk.Toplevel()
        dialog.focus()
        dialog.title("Search Reservations")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.config(bg=colors.BACKGROUND)
        
        name = tk.StringVar(dialog)
        
        def resetSearchButton() -> None:
            searchButton.config(fg=colors.FOREGROUND, text="Search")
        
        def error(text: str) -> None:
            searchButton.config(fg=colors.ERROR, text=text)
            dialog.after(1000, resetSearchButton)
        
        def tryMakeSearch() -> None:
            if name.get() == "":
                nameSearch = None
            elif not name.get().isalpha():
                error("Invalid name")
                return
            else:
                nameSearch = name.get().strip().lower()
            
            search = CustomerSearch(nameSearch)
            
            dialog.destroy()
            self.searchButton.config(state=tk.NORMAL)
            self.makeSearch(search)
            
        def close() -> None:
            self.searchButton.config(state=tk.NORMAL)
            dialog.destroy()
                            
        customerNameLabel = widgets.Label(dialog, text="Name", width=5)
        customerNameLabel.place(x=275, y=200, anchor="ne")
        customerNameEntry = widgets.Entry(dialog, textvariable=name, width=20)
        customerNameEntry.place(x=280, y=200)
        
        searchButton = widgets.Button(dialog, text="Search", width=20, height=2, command=tryMakeSearch)
        searchButton.place(x=280, y=560, anchor="sw")
        
        cancelButton = widgets.Button(dialog, text="Cancel", width=10, height=1, command=close)
        cancelButton.place(x=40, y=40)
        
        dialog.protocol("WM_DELETE_WINDOW", close)
        
        # Bind return key to press the search button.
        dialog.bind("<Return>", lambda e: tryMakeSearch())  # Lambda to resolve differing arguments.
        
        # Focus on first text entry to ready it for typing immediately.
        # After needed to resolve bug where using .focus() doesn't work.
        dialog.after(1, lambda: [dialog.focus_force(), customerNameEntry.focus()])