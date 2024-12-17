import tkinter as tk
import pickle
from hashing import hash
from typing import List, Dict
from Employee import Employee
import colors
import widgets

class Login(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        # Types explicitly stated for clarity.
        self.employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
        self.usernames: List[str] = [employee.username for employee in self.employees]
        self.passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        self.logInButtonText = tk.StringVar(value="Log In")
        
        logoImg = tk.PhotoImage(file="resources/diner.png")
        logo = tk.Label(self, image=logoImg, borderwidth=0)
        logo.place(x=400, y=40, anchor="n")
        
        userEntry = widgets.Entry(self, textvariable=self.username)
        userEntry.place(x=400, y=300, anchor="n")
        userLabel = widgets.Label(self, text="Username", width=8, height=1)
        userLabel.place(x=250, y=305, anchor="ne")
        
        passEntry = widgets.Entry(self, textvariable=self.password, show="*")
        passEntry.place(x=400, y=380, anchor="n")
        passLabel = widgets.Label(self, text="Password", width=8, height=1)
        passLabel.place(x=250, y=385, anchor="ne")
        
        # Log in button is the only widget that is a member field as it needs to be referred to later for error().
        self.logInButton = widgets.Button(self, textvariable=self.logInButtonText, width=20, height=2, command=self.logInButtonPress)
        self.logInButton.place(x=400, y=496, anchor="n")
        
        self.bind("<Return>", self.onReturn)
        
        self.mainloop()
        
    def error(self, message: str) -> None:
        # Display error message on log in button and remove after three seconds.
        self.logInButtonText.set(message)
        self.logInButton.config(fg=colors.ERROR)
        self.after(3000, self.resetLogInButton)
        
    def resetLogInButton(self) -> None:
        self.logInButtonText.set("Log In")
        self.logInButton.config(fg=colors.FOREGROUND)
        
    def onReturn(self, event: tk.Event) -> None:
        self.logInButtonPress()
        
    def logInButtonPress(self) -> None:
        username = self.username.get()
        password = self.password.get()
        
        if username == "":
            self.error("Username empty")
        elif password == "":
            self.error("Password empty")
        elif username not in self.usernames:
            self.error("Incorrect username")
        elif self.passwordHashes[username] != hash(password):
            self.error("Incorrect password")
        else:
            # Set user equal to employee object with username entered.
            # Validation was carried out earlier to ensure this never fails.
            user = self.employees[self.usernames.index(username)]
            
            self.destroy()  # Destroy this window as it is no longer needed.
            
            # Go to correct menu depending on type of user.
            # All windows from now on will take an extra "user" parameter so they know which user is logged in.
            if username == "colinr83":
                AdminMenu(user)
            else:
                EmployeeMenu(user)  
        
# Menus must be defined in same file to avoid circular imports.                
class AdminMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        logOutButton = widgets.Button(self, text="Log Out", width=10, height=2, command=self.logOut)
        logOutButton.place(x=15, y=15)
        
        tallyRevenueButton = widgets.Button(self, text="Tally Revenue", width=15, height=2, command=self.tallyRevenue)
        tallyRevenueButton.place(x=785, y=15, anchor="ne")
        
        makeReservationButton = widgets.Button(self, text="Make Reservation", width=20, height=2, command=self.makeReservation)
        makeReservationButton.place(x=380, y=120, anchor="ne")
        
        createMealButton = widgets.Button(self, text="Create Meal", width=20, height=2, command=self.createMeal)
        createMealButton.place(x=380, y=253, anchor="ne")
        
        addEmployeeButton = widgets.Button(self, text="Add Employee", width=20, height=2, command=self.addEmployee)
        addEmployeeButton.place(x=380, y=386, anchor="ne")
        
        viewReservationsButton = widgets.Button(self, text="View Reservations", width=20, height=2, command=self.viewReservations)
        viewReservationsButton.place(x=420, y=120, anchor="nw")
        
        viewMealsButton = widgets.Button(self, text="View Meals", width=20, height=2, command=self.viewMeals)
        viewMealsButton.place(x=420, y=253, anchor="nw")
        
        viewEmployeesButton = widgets.Button(self, text="View Employees", width=20, height=2, command=self.viewEmployees)
        viewEmployeesButton.place(x=420, y=386, anchor="nw")
        
        viewCustomersButton = widgets.Button(self, text="View Customers", width=20, height=2, command=self.viewCustomers)
        viewCustomersButton.place(x=400, y=510, anchor="n")
        
        self.after(3 * 60 * 1000, self.logOut)  # Return to login after three minutes of inactivity.
        self.bind("<Motion>", self.resetTimeOut)  # Reset timeout every time the mouse is moved.
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel("logOut")
        self.after(3 * 60 * 1000, self.logOut)
        
    def logOut(self) -> None:
        self.destroy()
        Login()
        
    def tallyRevenue(self) -> None:
        ...  # TODO: revenue tally 
        
    def makeReservation(self) -> None:
        ...  # TODO: reservation maker
        
    def createMeal(self) -> None:
        ...  # TODO: meal creator
        
    def addEmployee(self) -> None:
        ...  # TODO: employee adder
        
    def viewReservations(self) -> None:
        ...  # TODO: reservation viewer
        
    def viewMeals(self) -> None:
        ...  # TODO: meal viewer
        
    def viewEmployees(self) -> None:
        ...  # TODO: employee viewer
    
    def viewCustomers(self) -> None:
        ...  # TODO: customer viewer
        
class EmployeeMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.user = user
        
        self.mainloop()