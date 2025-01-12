import tkinter as tk
import pickle
from typing import List
from Employee import Employee
import colors
import widgets
import Login
from Reservation import Reservation
import AdminMenu
import EmployeeMenu


class ReservationViewer(tk.Tk):
    def __init__(self, user: Employee, listContents: List[Reservation] | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Reservation Viewer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        if listContents is None:
            listContents = pickle.load(open("data/reservations.dat", "rb"))
        
        listContents = sorted(listContents, key=lambda x: x.time)  # type: ignore
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=20, y=20)
        
        deleteButton = widgets.Button(self, text="Delete Selected", width=12, height=1, command=self.deleteSelected)
        deleteButton.place(x=400, y=20, anchor="n")
        
        searchButton = widgets.Button(self, text="Search...", )
        
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
        if self.user.username == "colinr83":
            AdminMenu.AdminMenu(self.user)
        else:
            EmployeeMenu.EmployeeMenu(self.user)
            
    def deleteSelected(self) -> None:
        ...