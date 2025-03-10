import pickle
from typing import List
from Order import Order
from Meal import Meal
from MealDB import MealDB
import ReservationDB

class OrderDB:
    def __init__(self) -> None:
        """Order database class. Create an instance of this class to interact with the database using its methods."""
        self.orders: List[Order] = pickle.load(open("data/orders.dat", "rb"))
        
    def add(self, reservationID: int, mealID: int) -> None:
        """Add an order with the given details."""
        if len(self.orders) == 0:
            orderID = 0
        else:
            orderID = self.orders[-1].orderID + 1
        
        self.orders.append(Order(orderID, reservationID, mealID))
        
        self.saveChanges()
        
    def getAssociatedMeals(self, reservationID: int) -> List[Meal]:
        """Returns a list of all meals associated with a given reservationID."""
        matches = []
        
        meals = MealDB()
        
        for order in self.orders:
            if order.reservationID == reservationID:
                matches.append(meals.getByID(order.mealID))
        
        return matches
        
    def deleteAssociated(self, reservationID: int) -> None:
        """Delete all orders associated with a given reservationID."""
        indexesToDelete = []
        
        for index, order in enumerate(self.orders):
            if order.reservationID == reservationID:
                indexesToDelete.append(index)
                
        indexesToDelete.reverse()  # Reverse so that indexes are not affected by deletions. 
                
        for index in indexesToDelete:
            del self.orders[index]
        
        self.saveChanges()
        
    def deleteAllWithMeal(self, mealID: int) -> None:
        """Delete all orders that order a meal with the given mealID."""
        reservations = ReservationDB.ReservationDB()
        
        while True:
            for order in self.orders:
                if order.mealID == mealID:
                    reservations.delete(order.reservationID)
                
            break  # If made a full run through the for loop, that means no more orders/reservations with this meal exist.
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/orders.dat", "wb") as file:
            pickle.dump(self.orders, file)