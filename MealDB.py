import pickle
from typing import List
from Meal import Meal
from MealSearch import MealSearch
import OrderDB
from helpers import binarySearch

class MealDB:
    def __init__(self) -> None:
        """Meal database class. Create an instance of this class to interact with the database using its methods."""
        self.meals: List[Meal] = pickle.load(open("data/meals.dat", "rb"))
        
    def findMatches(self, search: MealSearch) -> List[Meal]:
        """Returns all meals that match the given search."""
        matches = []
        
        for meal in self.meals:
            if search.matches(meal):
                matches.append(meal)
                
        return matches
        
    def add(self, name: str, price: float) -> None:
        """Add meal with the given details."""
        if len(self.meals) == 0:
            mealID = 0
        else:
            mealID = self.meals[-1].mealID + 1
        
        self.meals.append(Meal(mealID, name, price))
        
        self.saveChanges()
        
    def delete(self, mealID: int) -> None:
        """Delete the meal with the given mealID."""
        index = binarySearch(self.meals, mealID, lambda x: x.mealID)
        del self.meals[index]
            
        orders = OrderDB.OrderDB()
        orders.deleteAllWithMeal(mealID)
        
        self.saveChanges()
        
    def getByID(self, mealID: int) -> Meal:
        """Return the meal that has the given mealID."""
        index = binarySearch(self.meals, mealID, lambda x: x.mealID)
        
        if index == -1: raise ValueError(f"This exception is unreachable due to the validation elsewhere in my code.")
        
        return self.meals[index]
    
    def getByName(self, name: str) -> Meal:
        """Return the meal that has the given name."""
        for meal in self.meals:
            if meal.name == name:
                return meal
        
        raise ValueError(f"Meal with name {name} was not found.")
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to the database."""
        with open("data/meals.dat", "wb") as file:
            pickle.dump(self.meals, file)