import pickle
from typing import List, Tuple
from Order import Order
from Meal import Meal
from MealDB import MealDB
import ReservationDB

class OrderDB:
    def __init__(self) -> None:
        """Order database class. Create an instance of this class to interact with the database using its methods."""
        self.orders: List[Order] = pickle.load(open("data/orders.dat", "rb"))
        
    def add(self, reservationID: int, mealID: int, quantity: int) -> None:
        """Add an order with the given details."""
        if len(self.orders) == 0:
            orderID = 0
        else:
            orderID = self.orders[-1].orderID + 1
        
        self.orders.append(Order(orderID, reservationID, mealID, quantity))
        
        self.saveChanges()
        
    def getAssociatedMeals(self, reservationID: int) -> List[Tuple[Meal, int]]:
        """Returns a list of all meals associated with a given reservationID as tuples along with their respective
        quantities."""
        matches = []
        
        meals = MealDB()
        
        for order in self.orders:
            if order.reservationID == reservationID:
                matches.append((meals.getByID(order.mealID), order.quantity))
        
        return matches
        
    def deleteAssociated(self, reservationID: int) -> None:
        """Delete all orders associated with a given reservationID."""
        indicesToDelete = []
        
        for index, order in enumerate(self.orders):
            if order.reservationID == reservationID:
                indicesToDelete.append(index)
                
        indicesToDelete.reverse()  # Reverse so that indices are not affected by deletions. 
                
        for index in indicesToDelete:
            del self.orders[index]
        
        self.saveChanges()
        
    def deleteAllWithMeal(self, mealID: int) -> None:
        """Delete all orders that order a meal with the given mealID."""
        reservations = ReservationDB.ReservationDB()
        
        indicesToDelete = []
        
        for index, order in enumerate(self.orders):
            if order.mealID == mealID:
                indicesToDelete.append(index)
                
        indicesToDelete.reverse()  # Reverse so that indices are not affected by deletions.
        
        for index in indicesToDelete:
            del self.orders[index]
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/orders.dat", "wb") as file:
            pickle.dump(self.orders, file)