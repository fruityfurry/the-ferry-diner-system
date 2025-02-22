import pickle
from typing import List
from Meal import Meal
from MealSearch import MealSearch
import OrderDB
from binarySearch import binarySearch

class MealDB:
    def __init__(self) -> None:
        self.meals: List[Meal] = pickle.load(open("data/meals.dat", "rb"))
        
    def findMatches(self, search: MealSearch) -> List[Meal]:
        matches = []
        
        for meal in self.meals:
            if search.matches(meal):
                matches.append(meal)
                
        return matches
        
    def add(self, name: str, price: float) -> None:
        if len(self.meals) == 0:
            mealID = 0
        else:
            mealID = self.meals[-1].mealID + 1
        
        self.meals.append(Meal(mealID, name, price))
        
        self.saveChanges()
        
    def delete(self, mealID: int) -> None:
        index = binarySearch(self.meals, mealID, lambda x: x.mealID)
        del self.meals[index]
            
        orders = OrderDB.OrderDB()
        orders.deleteAllWithMeal(mealID)
        
        self.saveChanges()
        
    def getByID(self, mealID: int) -> Meal:
        index = binarySearch(self.meals, mealID, lambda x: x.mealID)
        
        if index == -1: raise ValueError(f"Meal with ID {mealID} was not found.")
        
        return self.meals[index]
    
    def getByName(self, name: str) -> Meal:
        for meal in self.meals:
            if meal.name == name:
                return meal
        
        raise ValueError(f"Meal with name {name} was not found.")
        
    def saveChanges(self) -> None:
        with open("data/meals.dat", "wb") as file:
            pickle.dump(self.meals, file)