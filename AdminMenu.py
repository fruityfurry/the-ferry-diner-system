import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import ReservationMaker
import ReservationViewer
import MealCreator
import MealViewer
import EmployeeAdder
import EmployeeViewer
import CustomerViewer
import RevenueTally

# All windows in my system exist as classes that inherit from tk.TK (the tkinter class for a window).
# Only one instance of these will exist at a time, naturally, but subclassing tk.Tk allows for incredibly powerful
# compartmentalisation. All local variables can exist as member variables of the class, leaving the global namespace
# completely clutter-free.

class AdminMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        """The admin menu. Only colin (colinr83) can access this."""
        
        super().__init__(*args, **kwargs)
        self.title("Admin Menu")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        logOutButton = widgets.Button(self, text="Log Out", width=10, height=2, command=self.logOut)
        logOutButton.place(x=15, y=15)
        
        tallyRevenueButton = widgets.Button(self, text="Tally Revenue", width=15, height=2, command=self.tallyRevenue)
        tallyRevenueButton.place(x=785, y=15, anchor="ne")
        
        makeReservationButton = widgets.Button(self, text="Make Reservation", width=20, height=2,
                                               command=self.makeReservation)
        makeReservationButton.place(x=380, y=120, anchor="ne")
        
        createMealButton = widgets.Button(self, text="Create Meal", width=20, height=2, command=self.createMeal)
        createMealButton.place(x=380, y=253, anchor="ne")
        
        addEmployeeButton = widgets.Button(self, text="Add Employee", width=20, height=2, command=self.addEmployee)
        addEmployeeButton.place(x=380, y=386, anchor="ne")
        
        viewReservationsButton = widgets.Button(self, text="View Reservations", width=20, height=2,
                                                command=self.viewReservations)
        viewReservationsButton.place(x=420, y=120, anchor="nw")
        
        viewMealsButton = widgets.Button(self, text="View Meals", width=20, height=2, command=self.viewMeals)
        viewMealsButton.place(x=420, y=253, anchor="nw")
        
        viewEmployeesButton = widgets.Button(self, text="View Employees", width=20, height=2, command=self.viewEmployees)
        viewEmployeesButton.place(x=420, y=386, anchor="nw")
        
        viewCustomersButton = widgets.Button(self, text="View Customers", width=20, height=2, command=self.viewCustomers)
        viewCustomersButton.place(x=400, y=510, anchor="n")
        
        # Return to login after three minutes of inactivity.
        self.timeout = self.after(2 * 60 * 1000, self.logOut)  # Store to member variable so this can be cancelled later.
        self.bind("<Motion>", self.resetTimeOut)  # Reset timeout every time the mouse is moved.
        
        # Bind escape key to return to login.
        self.bind("<Escape>", lambda e: self.logOut())  # Lambda to resolve differing arguments.
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel(self.timeout)
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        
    # Timeout function is cancelled before going to any other window to prevent non-fatal but annoying errors in the console.
    def logOut(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        Login.Login()
        
    def tallyRevenue(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        RevenueTally.RevenueTally(self.user)
        
    def makeReservation(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        ReservationMaker.ReservationMaker(self.user)
        
    def createMeal(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        MealCreator.MealCreator(self.user)
        
    def addEmployee(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        EmployeeAdder.EmployeeAdder(self.user)
        
    def viewReservations(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        ReservationViewer.ReservationViewer(self.user)
        
    def viewMeals(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        MealViewer.MealViewer(self.user)
        
    def viewEmployees(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        EmployeeViewer.EmployeeViewer(self.user)
    
    def viewCustomers(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        CustomerViewer.CustomerViewer(self.user)