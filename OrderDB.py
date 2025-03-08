import pickle
from typing import List
from Order import Order
from Meal import Meal
from MealDB import MealDB
import ReservationDB

class OrderDB:
    def __init__(self) -> None:
        self.orders: List[Order] = pickle.load(open("data/orders.dat", "rb"))
        
    def add(self, reservationID: int, mealID: int) -> None:
        if len(self.orders) == 0:
            orderID = 0
        else:
            orderID = self.orders[-1].orderID + 1
        
        self.orders.append(Order(orderID, reservationID, mealID))
        
        self.saveChanges()
        
    def getAssociatedMeals(self, reservationID: int) -> List[Meal]:
        matches = []
        
        meals = MealDB()
        
        for order in self.orders:
            if order.reservationID == reservationID:
                matches.append(meals.getByID(order.mealID))
        
        return matches
        
    def deleteAssociated(self, reservationID: int) -> None:
        indexesToDelete = []
        
        for index, order in enumerate(self.orders):
            if order.reservationID == reservationID:
                indexesToDelete.append(index)
                
        indexesToDelete.reverse()  # Reverse so that indexes are not affected by deletions. 
                
        for index in indexesToDelete:
            del self.orders[index]
        
        self.saveChanges()
        
    def deleteAllWithMeal(self, mealID: int) -> None:
        reservations = ReservationDB.ReservationDB()
        
        while True:
            for order in self.orders:
                if order.mealID == mealID:
                    reservations.delete(order.reservationID)
                    continue
                
            break  # If made a full run through the for loop, that means no more orders/reservations with this meal exist.
        
    def saveChanges(self) -> None:
        with open("data/orders.dat", "wb") as file:
            pickle.dump(self.orders, file)