import tkinter as tk
from EmployeeDB import EmployeeDB
from PasswordDB import PasswordDB
import colors
import widgets
import AdminMenu
import EmployeeMenu



class Login(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        logoImg = tk.PhotoImage(file="resources/diner.png", master=self)
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
        self.logInButton = widgets.Button(self, text="Log In", width=20, height=2, command=self.logInButtonPress)
        self.logInButton.place(x=400, y=496, anchor="n")
        
        # Bind return key to function.
        self.bind("<Return>", self.onReturn)
        
        self.mainloop()
        
    def error(self, text: str) -> None:
        # Display error message on log in button and remove after one second.
        self.logInButton.config(text=text, fg=colors.ERROR)
        self.after(1000, self.resetLogInButton)
        
    def resetLogInButton(self) -> None:
        # Reset log in button.
        self.logInButton.config(text="Log In", fg=colors.FOREGROUND)
        
    def onReturn(self, event: tk.Event) -> None:
        # Quality of life feature, press log in button if return key is pressed.
        self.logInButtonPress()
        
    def logInButtonPress(self) -> None:
        # Load up databases.
        employees = EmployeeDB()
        passwords = PasswordDB()
        
        username = self.username.get()
        password = self.password.get()
        
        # Validation.
        if username == "":
            self.error("Username empty")
        elif password == "":
            self.error("Password empty")
        elif not employees.exists(username):
            self.error("Username does not exist")
        elif not passwords.passwordIsCorrect(username, password):
            self.error("Incorrect password")
        else:
            # Set user equal to employee object with username entered.
            # Validation was carried out earlier to ensure this function call never fails.
            user = employees.getByUsername(username)
            
            self.destroy()  # Destroy this window as it is no longer needed.
            
            # Go to correct menu depending on type of user.
            # All windows from now on will take an extra "user" parameter so they know which user is logged in.
            if username == "colinr83":
                AdminMenu.AdminMenu(user)
            else:
                EmployeeMenu.EmployeeMenu(user)