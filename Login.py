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
        
        self.employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
        self.usernames: List[str] = [employee.name for employee in self.employees]
        self.passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        self.logInButtonText = tk.StringVar(value="Log In")
        
        logoImg = tk.PhotoImage(file="resources/diner.png")
        logo = tk.Label(self, image=logoImg, borderwidth=0)
        logo.place(x=400, y=40, anchor="n")
        
        userEntry = widgets.Entry(self, textvariable=self.username)
        userEntry.place(x=400, y=300, anchor="n")
        
        passEntry = widgets.Entry(self, textvariable=self.password, show="*")
        passEntry.place(x=400, y=380, anchor="n")
        
        # Log in button is the only widget that is a member field as it needs to be referred to later for error().
        self.logInButton = widgets.Button(self, textvariable=self.logInButtonText, width=20, height=2, command=self.logInButtonPress)
        self.logInButton.place(x=400, y=496, anchor="n")
        
        self.mainloop()
        
    def error(self, message: str) -> None:
        """
        Display error message on log in button and remove after three seconds.
        """
        self.logInButtonText.set(message)
        self.logInButton.config(fg=colors.ERROR)
        self.after(3000, self.resetLogInButton)
        
    def resetLogInButton(self) -> None:
        self.logInButtonText.set("Log In")
        self.logInButton.config(fg=colors.FOREGROUND)
        
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
            ...