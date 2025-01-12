import pickle
from typing import List
from Reservation import Reservation
from ReservationSearch import ReservationSearch
from Meal import Meal
from OrderDB import OrderDB

class ReservationDB:
    def __init__(self) -> None:
        self.reservations: List[Reservation] = pickle.load(open("data/reservations.dat", "rb"))
        
    def findMatches(self, search: ReservationSearch) -> List[Reservation]:
        matches = []
        
        for reservation in self.reservations:
            if search.matches(reservation):
                matches.append(reservation)
                
        return matches
    
    def add(self, customerID: int, employeeUser: str, time: str, peopleNum: int, meals: List[Meal]) -> None:
        reservationID = self.reservations[-1].reservationID + 1  # Reservations are stored in ascending PK order so this will
                                                                 # always produce a unique ID.

        self.reservations.append(Reservation(reservationID, customerID, employeeUser, time, peopleNum))
        
        orders = OrderDB()
        
        for meal in meals:
            orders.add(reservationID, meal.mealID)
            
        self.saveChanges()
        
    def delete(self, reservationID: int) -> None:
        for reservation in self.reservations:
            if reservation.reservationID == reservationID:
                self.reservations.remove(reservation)
                break
            
        orders = OrderDB()
        orders.deleteAssociated(reservationID)
        
        self.saveChanges()
        
    def saveChanges(self) -> None:
        with open("data/reservations.dat", "wb") as file:
            pickle.dump(self.reservations, file)