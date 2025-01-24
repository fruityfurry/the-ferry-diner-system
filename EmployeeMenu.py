import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import ReservationMaker
import ReservationViewer

class EmployeeMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Menu")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        logOutButton = widgets.Button(self, text="Log Out", width=10, height=2, command=self.logOut)
        logOutButton.place(x=15, y=15)
        
        makeReservationButton = widgets.Button(self, text="Make Reservation", width=20, height=2, command=self.makeReservation)
        makeReservationButton.place(x=140, y=294)
        
        viewReservationsButton = widgets.Button(self, text="View Reservations", width=20, height=2, command=self.viewReservations)
        viewReservationsButton.place(x=420, y=294)
        
        # Return to login after three minutes of inactivity.
        self.timeout = self.after(2 * 60 * 1000, self.logOut)  # Store to member variable so this can be cancelled later.
        self.bind("<Motion>", self.resetTimeOut)  # Reset timeout every time the mouse is moved.
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel(self.timeout)
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        
    def logOut(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        Login.Login()
        
    def makeReservation(self) -> None:
        self.destroy()
        ReservationMaker.ReservationMaker(self.user)
        
    def viewReservations(self) -> None:
        self.destroy()
        ReservationViewer.ReservationViewer(self.user)