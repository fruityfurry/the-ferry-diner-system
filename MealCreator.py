import tkinter as tk
from Employee import Employee
import colors
import widgets
import Login
import AdminMenu
from MealDB import MealDB

class MealCreator(tk.Tk):
    def __init__(self, user: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Meal Creator")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=colors.BACKGROUND)
        
        self.user = user
        
        self.meals = MealDB()
        
        self.name = tk.StringVar(self)
        self.price = tk.StringVar(self)
        
        backButton = widgets.Button(self, text="Back", width=8, height=1, command=self.returnToMenu)
        backButton.place(x=40, y=40)
        
        nameLabel = widgets.Label(self, text="Meal Name", width=10)
        nameLabel.place(x=275, y=200, anchor="ne")
        nameEntry = widgets.Entry(self, textvariable=self.name, width=20)
        nameEntry.place(x=280, y=200)
        
        priceLabel = widgets.Label(self, text="Price £", width=8)
        priceLabel.place(x=275, y=300, anchor="ne")
        priceEntry = widgets.Entry(self, textvariable=self.price, width=20)
        priceEntry.place(x=280, y=300)
        
        self.createMealButton = widgets.Button(self, text="Create Meal", width=20, height=2, command=self.createMeal)
        self.createMealButton.place(x=280, y=560, anchor="sw")
        
        self.timeout = self.after(2 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        # Bind return key to press the create meal button.
        self.bind("<Return>", lambda e: self.createMeal())  # Lambda to resolve differing arguments.
        
        # Bind escape key to return to menu.
        self.bind("<Escape>", lambda e: self.returnToMenu())  # Lambda to resolve differing arguments.
        
        # Focus on first text entry to ready it for typing immediately.
        # After needed to resolve bug where using .focus() doesn't work.
        self.after(1, lambda: [self.focus_force(), nameEntry.focus()])
        
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
        
    def resetCreateMealButton(self) -> None:
        self.createMealButton.config(text="Create Meal", fg=colors.FOREGROUND)
        
    def error(self, text: str) -> None:
        self.createMealButton.config(text=text, fg=colors.ERROR)
        self.after(1000, self.resetCreateMealButton)
        
    def createMeal(self) -> None:
        name = self.name.get().strip()
        price = self.price.get().strip()
        
        if name == "":
            self.error("Name empty")
        elif len(name) > 50:
            self.error("Name too long")
        elif not name.replace(" ", "").isalpha(): # Spaces are not alpha but we allow them, so we remove them for this check.
            self.error("Invalid name")
        elif "." in price and len(price.split(".")[1]) > 2:
            self.error("Too many decimal places")
        else:
            try:
                price = round(float(price), 2)
                if not 0 < price < 100:
                    self.error("Invalid price")
                    return
            except:
                self.error("Invalid price")
                return
            
            self.meals.add(name, price)
            
            self.createMealButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
            self.after(1000, self.returnToMenu)