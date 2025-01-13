import pickle
from typing import List
from Reservation import Reservation
from ReservationSearch import ReservationSearch
from Meal import Meal
from OrderDB import OrderDB
from CustomerDB import CustomerDB
from EmployeeDB import EmployeeDB

class ReservationDB:
    def __init__(self) -> None:
        self.reservations: List[Reservation] = pickle.load(open("data/reservations.dat", "rb"))
        
    def findMatches(self, search: ReservationSearch) -> List[Reservation]:
        matches = []
        customers = CustomerDB()
        employees = EmployeeDB()
        
        for reservation in self.reservations:
            if search.matches(reservation):
                if search.customerSearch is not None:
                    customer = customers.getByID(reservation.customerID)
                    if f"{customer.fName} {customer.sName}".lower().find(search.customerSearch) == -1:
                        continue
                    
                if search.employeeSearch is not None:
                    employee = employees.getByUsername(reservation.employeeUser)
                    if employee.name.find(search.employeeSearch.lower()) == -1:
                        continue
                
                matches.append(reservation)
                
        return matches
    
    def add(self, customerID: int, employeeUser: str, time: str, peopleNum: int, meals: List[Meal]) -> None:
        if len(self.reservations) == 0:
            reservationID = 0
        else:
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
        
    def getAssociatedMeals(self, reservationID: int) -> List[Meal]:
        orders = OrderDB()
        return orders.getAssociatedMeals(reservationID)
        
    def saveChanges(self) -> None:
        with open("data/reservations.dat", "wb") as file:
            pickle.dump(self.reservations, file)