import tkinter as tk
import pickle
from Employee import Employee
import colors
import widgets

class EmployeeMenu(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.user = user
        
        self.mainloop()