import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
from EmployeeSearch import EmployeeSearch
from EmployeeDB import EmployeeDB
import re
from PasswordDB import PasswordDB
from ReservationDB import ReservationDB
from helpers import hash, quicksort

class EmployeeViewer(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        """Employee viewer window."""
        super().__init__(*args, **kwargs)
        self.title("Employee Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.employeeDB = EmployeeDB()
        self.employees = [x for x in self.employeeDB.employees]  # To avoid passing by reference and removing
                                                                 # the admin account from the database as well.
        self.employees.remove(self.employeeDB.getByUsername("colinr83"))  # Do not display the admin account.
        quicksort(self.employees, lambda x: x.name)
        
        self.sortBy = tk.StringVar(self, "Name")
        self.sortBy.trace_add("write", self.sortByChanged)
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        self.numSelectedLabel = widgets.Label(self, text="0 Selected", width=10, height=1)
        self.numSelectedLabel.place(x=400, y=25, anchor="n")
        
        sortByLabel = widgets.Label(self, text="Sort by ", width=9, height=1)
        sortByLabel.place(x=480, y=25)
        sortByDropdown = widgets.Dropdown(self, self.sortBy, *["Name", "Username", "Reservations"])
        sortByDropdown.config(width=12)
        sortByDropdown.place(x=780, y=20, anchor="ne")
        
        self.listbox = widgets.Listbox(self, width=63, height=18)
        self.listbox.bind("<<ListboxSelect>>", self.updateNumSelected)
        self.listbox.place(x=20, y=80)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=14, height=1, command=self.deleteSelected)
        deleteButton.place(x=20, y=580, anchor="sw")
        
        self.changePasswordButton = widgets.Button(self, text="Change Password", width=20, height=1,
                                                   command=self.changePasswordDialog)
        self.changePasswordButton.place(x=400, y=580, anchor="s")
        
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
            
    def resetChangePasswordButton(self) -> None:
        self.changePasswordButton.config(text="Change Password", fg=colors.FOREGROUND)
        
    def error(self, text: str) -> None:
        self.changePasswordButton.config(text=text, fg=colors.ERROR)
        self.after(1000, self.resetChangePasswordButton)
            
    def updateNumSelected(self, event: tk.Event | None) -> None:
        self.numSelectedLabel.config(text=f"{len(self.listbox.curselection())} Selected")
            
    def sortByChanged(self, varName: str, index: str, action: str) -> None:
        self.sort()
    
    def sort(self) -> None:
        # Sort by appropriate attribute depending on selection.
        if self.sortBy.get() == "Name":
            quicksort(self.employees, lambda x: x.name)
        elif self.sortBy.get() == "Username":
            quicksort(self.employees, lambda x: x.username)
        elif self.sortBy.get() == "Reservations":
            quicksort(self.employees, lambda x: x.reservationsMade)
            
        self.updateListbox()
        self.updateNumSelected(None)
            
    def updateListbox(self) -> None:
        """Update the listbox.
        This function must be called whenever the underlying list is changed, otherwise it will not display correctly."""
        lines = []
        
        for employee in self.employees:
            lines.append(f"{employee.name} - {employee.username} - {employee.reservationsMade} reservations")
            
        # Delete all old lines and put in the new ones.
        self.listbox.delete(0, tk.END)
        self.listbox.insert(0, *lines)
        
    def getSelected(self) -> List[Employee]:
        indices: Tuple[int] = self.listbox.curselection()
        
        return [self.employees[index] for index in indices]
            
    def deleteSelected(self) -> None:
        selected = self.getSelected()
        
        if len(selected) > 0 and messagebox.askyesno("Are you sure?",
                                                     f"Are you sure you want to delete {len(selected)} employees?"):
            reservationDB = ReservationDB()
            
            for employee in selected:
                if reservationDB.employeeHasReservations(employee.username):
                    messagebox.showerror("Deletion cancelled", f"{employee.name} has existing reservations!")
                    return
                
                self.employeeDB.delete(employee.username)
                self.employees.remove(employee)
                
            self.updateListbox()
            self.updateNumSelected(None)
        
    def makeSearch(self, search: EmployeeSearch) -> None:
        self.employees = self.employeeDB.findMatches(search)  # This function never returns the admin account so no need to
                                                              # remove it.
        self.sort()  # Sort updates listbox itself, so no need to call it.
        
    def searchDialog(self) -> None:
        self.searchButton.config(state=tk.DISABLED)
        
        # Open new window for search dialog.
        dialog = tk.Toplevel()
        dialog.focus()
        dialog.title("Search Reservations")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.config(bg=colors.BACKGROUND)
        
        username = tk.StringVar(dialog)
        name = tk.StringVar(dialog)
        
        def resetSearchButton() -> None:
            searchButton.config(fg=colors.FOREGROUND, text="Search")
        
        def error(text: str) -> None:
            searchButton.config(fg=colors.ERROR, text=text)
            dialog.after(1000, resetSearchButton)
        
        def tryMakeSearch() -> None:
            if username.get() == "":
                usernameSearch = None
            else:
                usernameSearch = username.get().strip()
                
            if name.get() == "":
                nameSearch = None
            elif not name.get().isalpha():
                error("Invalid name")
                return
            else:
                nameSearch = name.get().strip()
            
            search = EmployeeSearch(usernameSearch=usernameSearch, nameSearch=nameSearch)
            
            dialog.destroy()
            self.searchButton.config(state=tk.NORMAL)
            self.makeSearch(search)
            
        def close() -> None:
            self.searchButton.config(state=tk.NORMAL)
            dialog.destroy()
                            
        nameLabel = widgets.Label(dialog, text="Name", width=6)
        nameLabel.place(x=275, y=40, anchor="ne")
        nameEntry = widgets.Entry(dialog, textvariable=name, width=20)
        nameEntry.place(x=280, y=40)
        
        usernameLabel = widgets.Label(dialog, text="Username", width=13)
        usernameLabel.place(x=275, y=160, anchor="ne")
        usernameEntry = widgets.Entry(dialog, textvariable=username, width=20)
        usernameEntry.place(x=280, y=160)
        
        searchButton = widgets.Button(dialog, text="Search", width=20, height=2, command=tryMakeSearch)
        searchButton.place(x=280, y=560, anchor="sw")
        
        cancelButton = widgets.Button(dialog, text="Cancel", width=10, height=1, command=close)
        cancelButton.place(x=40, y=560, anchor="sw")
        
        dialog.protocol("WM_DELETE_WINDOW", close)
        
        # Bind return key to press the search button.
        dialog.bind("<Return>", lambda e: tryMakeSearch())  # Lambda to resolve differing arguments.
        
        # Focus on first text entry to ready it for typing immediately.
        # After needed to resolve bug where using .focus() doesn't work.
        dialog.after(1, lambda: [dialog.focus_force(), nameEntry.focus()])
        
    def changePasswordDialog(self) -> None:
        selected = self.getSelected()
        
        if len(selected) == 0:
            self.error("Select an Employee")
            return
        if len(selected) > 1:
            self.error("Select only one\nEmployee")
            return
        
        self.changePasswordButton.config(state=tk.DISABLED)
        
        selectedEmployee = selected[0]
        
        dialog = tk.Toplevel()
        dialog.focus()
        dialog.title("Change Password")
        dialog.geometry("800x600")
        dialog.config(bg=colors.BACKGROUND)
        
        password1 = tk.StringVar(dialog)
        password2 = tk.StringVar(dialog)
        
        def resetChangePasswordButton() -> None:
            changePasswordButton.config(text="Change Password", fg=colors.FOREGROUND)
            
        def error(text: str) -> None:
            changePasswordButton.config(text=text, fg=colors.ERROR)
            dialog.after(1000, resetChangePasswordButton)
        
        def tryMakeSearch() -> None:
            uppercaseLetters = "[A-Z]"
            numbers = "[0-9]"
            symbols = r"[!£$%^&*@?<>\-=_+]"
            disallowed = r"[ \[\]\{\}\(\)\\\|,.]"
            
            passwords = PasswordDB()
        
            if len(password1.get()) < 7:
                error("Password too short")
            elif len(password1.get()) > 40:
                error("Password too long")
            elif re.findall(uppercaseLetters, password1.get()) == []:
                error("Password must contain at\nleast 1 uppercase letter")
            elif re.findall(numbers, password1.get()) == []:
                error("Password must contain at\nleast 1 number")
            elif re.findall(symbols, password1.get()) == []:
                error("Password must contain at\nleast 1 symbol")
            elif re.findall(disallowed, password1.get()) != []:
                error("Password contains\ndisallowed characters")
            elif password1.get() != password2.get():
                error("Passwords must match")
            elif hash(password1.get()) == passwords.passwordHashes[selectedEmployee.username]:
                error("Password must be different\n from original")
            elif messagebox.askyesno("Confirm", f"Are you sure you want to change {selectedEmployee.name}'s password?"):
                passwords.add(selectedEmployee.username, password1.get())
                
                changePasswordButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
                dialog.after(1000, close)
                
        def close() -> None:
            self.changePasswordButton.config(state=tk.NORMAL)
            dialog.destroy()
                            
        password1Label = widgets.Label(dialog, text="New Password", width=13)
        password1Label.place(x=275, y=40, anchor="ne")
        password1Entry = widgets.Entry(dialog, textvariable=password1, width=20, show="*")
        password1Entry.place(x=280, y=40)
        
        password2Label = widgets.Label(dialog, text="Re-enter Password", width=18)
        password2Label.place(x=275, y=160, anchor="ne")
        password2Entry = widgets.Entry(dialog, textvariable=password2, width=20, show="*")
        password2Entry.place(x=280, y=160)
        
        changePasswordButton = widgets.Button(dialog, text="Change Password", width=20, height=2, command=tryMakeSearch)
        changePasswordButton.place(x=280, y=560, anchor="sw")
        
        cancelButton = widgets.Button(dialog, text="Cancel", width=10, height=1, command=close)
        cancelButton.place(x=40, y=560, anchor="sw")
        
        dialog.protocol("WM_DELETE_WINDOW", close)