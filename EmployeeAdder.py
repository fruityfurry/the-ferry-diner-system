import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
from EmployeeDB import EmployeeDB
import re

class EmployeeAdder(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Adder")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.name = tk.StringVar(self)
        self.username = tk.StringVar(self)
        self.password = tk.StringVar(self)
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=40, y=40)
        
        nameLabel = widgets.Label(self, text="Employee Name", width=14)
        nameLabel.place(x=275, y=165, anchor="ne")
        nameEntry = widgets.Entry(self, textvariable=self.name, width=20)
        nameEntry.place(x=280, y=165)
        
        usernameLabel = widgets.Label(self, text="Username", width=9)
        usernameLabel.place(x=275, y=265, anchor="ne")
        usernameEntry = widgets.Entry(self, textvariable=self.username, width=20)
        usernameEntry.place(x=280, y=265)
        
        passwordLabel = widgets.Label(self, text="Password", width=9)
        passwordLabel.place(x=275, y=365, anchor="ne")
        passwordEntry = widgets.Entry(self, textvariable=self.password, width=20, show="*")
        passwordEntry.place(x=280, y=365)
        
        self.addEmployeeButton = widgets.Button(self, text="Add Employee", width=20, height=2, command=self.addEmployee)
        self.addEmployeeButton.place(x=280, y=560, anchor="sw")
        
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
        AdminMenu.AdminMenu(self.user)  # This is an admin window so always return to admin menu.
        
    def resetAddEmployeeButton(self) -> None:
        self.addEmployeeButton.config(fg=colors.FOREGROUND, text="Create Meal")
        
    def error(self, text: str) -> None:
        self.addEmployeeButton.config(fg=colors.ERROR, text=text)
        self.after(1000, self.resetAddEmployeeButton)
        
    def addEmployee(self) -> None:
        employees = EmployeeDB()
        
        uppercaseLetters = "[A-Z]"
        numbers = "[0-9]"
        symbols = "[!£$%^&*@?<>]"

        name = self.name.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        
        if name == "":
            self.error("Name empty")
        elif len(name) > 50:
            self.error("Name too long")
        elif not name.replace(" ", "").isalpha():  # Spaces are not alpha, but we allow them, so we remove them for this check.
            self.error("Invalid name")
        elif username == "":
            self.error("Username empty")
        elif len(username) > 20:
            self.error("Name too long")
        elif employees.exists(username):
            self.error("Username taken")
        elif len(password) < 7:
            self.error("Password too short")
        elif len(password) > 40:
            self.error("Password too long")
        elif re.findall(uppercaseLetters, password) == []:
            self.error("Password must contain at\nleast 1 uppercase letter")
        elif re.findall(numbers, password) == []:
            self.error("Password must contain at\nleast 1 number")
        elif re.findall(symbols, password) == []:
            self.error("Password must contain at\nleast 1 symbol")
        else:
            
            employees.add(username, name, password)
            
            self.addEmployeeButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
            self.after(1000, self.returnToMenu)