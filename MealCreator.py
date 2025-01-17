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
        
        priceLabel = widgets.Label(self, text="Price", width=6)
        priceLabel.place(x=275, y=300, anchor="ne")
        priceEntry = widgets.Entry(self, textvariable=self.price, width=20)
        priceEntry.place(x=280, y=300)
        
        self.createMealButton = widgets.Button(self, text="Create Meal", width=20, height=2, command=self.createMeal)
        self.createMealButton.place(x=280, y=560, anchor="sw")
        
        self.timeout = self.after(3 * 60 * 1000, self.logOut)
        self.bind("<Motion>", self.resetTimeOut)
        
        self.mainloop()
        
    def resetTimeOut(self, event: tk.Event) -> None:
        # Cancel timeout and start timer again.
        self.after_cancel(self.timeout)
        self.timeout = self.after(3 * 60 * 1000, self.logOut)
        
    def logOut(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        Login.Login()
        
    def returnToMenu(self) -> None:
        self.after_cancel(self.timeout)
        self.destroy()
        AdminMenu.AdminMenu(self.user)  # This is an admin window so always return to admin menu.
        
    def resetCreateMealButton(self) -> None:
        self.createMealButton.config(fg=colors.FOREGROUND, text="Create Meal")
        
    def error(self, text: str) -> None:
        self.createMealButton.config(fg=colors.ERROR, text=text)
        self.after(1000, self.resetCreateMealButton)
        
    def createMeal(self) -> None:
        name = self.name.get().strip()
        price = self.price.get().strip()
        
        if name == "":
            self.error("Name empty")
        elif len(name) > 50:
            self.error("Name too long")
        elif not name.replace(" ", "").isalpha():  # Spaces are not alpha, but we allow them, so we remove them for this check.
            self.error("Invalid name")
        else:
            try:
                price = float(price)
                if price <= 0 or price >= 100:
                    self.error("Invalid price")
                    return
            except:
                self.error("Invalid price")
                return
            
            self.meals.add(name, price)
            
            self.createMealButton.config(text="Success!", disabledforeground=colors.HIGHLIGHT, state=tk.DISABLED)
            self.after(1000, self.returnToMenu)