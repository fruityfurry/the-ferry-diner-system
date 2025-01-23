import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
from OrderDB import OrderDB
from ReservationDB import ReservationDB

class RevenueTally(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Revenue Tally")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=40, y=40)
        
        tallyText = widgets.Label(self, width=50, height=10, justify=tk.CENTER)
        tallyText.place(x=400, y=300, anchor="center")
        
        revenue = 0
        meals = 0
        reservationNum = 0
        
        reservations = ReservationDB()
        orders = OrderDB()
        
        for reservation in reservations.reservations:
            reservationNum += 1
            
            for meal in orders.getAssociatedMeals(reservation.reservationID):
                meals += 1
                revenue += meal.price
                
        tallyText.config(text=f"Made £{round(revenue, 2)}\nfrom {meals} meals\nserved across {reservationNum} reservations today.")
        
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
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