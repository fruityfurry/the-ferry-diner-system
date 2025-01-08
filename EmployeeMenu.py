import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import ReservationMaker

class EmployeeMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.user = user
        
        self.mainloop()