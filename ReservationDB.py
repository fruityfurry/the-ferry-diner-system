import pickle
from typing import List
from Reservation import Reservation
from ReservationSearch import ReservationSearch
from Meal import Meal
from OrderDB import OrderDB
import CustomerDB
from EmployeeDB import EmployeeDB
from helpers import binarySearch

class ReservationDB:
    def __init__(self) -> None:
        """Reservation database class. Create an instance of this class to interact with the database using its methods."""
        self.reservations: List[Reservation] = pickle.load(open("data/reservations.dat", "rb"))
        
    def findMatches(self, search: ReservationSearch) -> List[Reservation]:
        """Returns all reservations that match the given search."""
        matches = []
        customers = CustomerDB.CustomerDB()
        employees = EmployeeDB()
        
        for reservation in self.reservations:
            if search.matches(reservation):
                # Customer and employee searches must be done outside ReservationSearch method to avoid circular imports.
                if search.customerSearch is not None:
                    customer = customers.getByID(reservation.customerID)
                    # If customer search cannot be found as a substring (case insensitive) in the customer's full name,
                    # no match.
                    if f"{customer.fName} {customer.sName}".lower().find(search.customerSearch.lower()) == -1:
                        continue
                    
                if search.employeeSearch is not None:
                    employee = employees.getByUsername(reservation.employeeUser)
                    # If employee search cannot be found as a substring (case insensitive) in the employee's full name,
                    # no match.
                    if employee.name.lower().find(search.employeeSearch.lower()) == -1:
                        continue
                
                matches.append(reservation)
                
        return matches
    
    def add(self, customerID: int, employeeUser: str, time: str, peopleNum: int, meals: List[Meal]) -> None:
        """Add reservation with the given details."""
        if len(self.reservations) == 0:
            reservationID = 0
        else:
            reservationID = self.reservations[-1].reservationID + 1  # Reservations are stored in ascending PK order so this
                                                                     # will always produce a unique ID.

        self.reservations.append(Reservation(reservationID, customerID, employeeUser, time, peopleNum))
        
        orders = OrderDB()
        
        # Add required order entries.
        for meal in meals:
            orders.add(reservationID, meal.mealID)
            
        self.saveChanges()
        
    def delete(self, reservationID: int) -> None:
        """Delete the reservation with the given reservationID."""
        index = binarySearch(self.reservations, reservationID, lambda x: x.reservationID)
        
        if index == -1: raise ValueError(f"Reservation with reservationID {reservationID} not found.")
                                         
        del self.reservations[index]
            
        orders = OrderDB()
        orders.deleteAssociated(reservationID)
        
        self.saveChanges()
        
    def deleteAssociated(self, customerID: int) -> None:
        """Delete all reservations that a customer with the given customerID has made."""
        reservationsIDs = []
        
        for reservation in self.reservations:
            if reservation.customerID == customerID:
                reservationsIDs.append(reservation.reservationID)
                self.reservations.remove(reservation)
                break
            
        orders = OrderDB()
        
        for reservationID in reservationsIDs:
            orders.deleteAssociated(reservationID)
        
        self.saveChanges()
        
    def getAssociatedMeals(self, reservationID: int) -> List[Meal]:
        """Returns a list of all meals that a given reservation has ordered."""
        orders = OrderDB()
        return orders.getAssociatedMeals(reservationID)
    
    def employeeHasReservations(self, user: str) -> bool:
        """Returns True if the given employee has made any existing reservations."""
        for reservation in self.reservations:
            if reservation.employeeUser == user:
                return True
            
        return False
    
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/reservations.dat", "wb") as file:
            pickle.dump(self.reservations, file)