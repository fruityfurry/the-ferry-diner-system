import pickle
from typing import List
from Employee import Employee
from PasswordDB import PasswordDB
from EmployeeSearch import EmployeeSearch

class EmployeeDB:
    def __init__(self) -> None:
        """Employee database class. Create an instance of this class to interact with the database using its methods."""
        self.employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
        
    def add(self, username: str, name: str, password: str) -> None:
        """Add employee with given details."""
        self.employees.append(Employee(username, name, 0))
        
        passwords = PasswordDB()
        passwords.add(username, password)
            
        self.saveChanges()
    
    def delete(self, username: str) -> None:
        """Delete the employee with the given username."""
        for employee in self.employees:
            if employee.username == username:
                self.employees.remove(employee)
                break
            
        passwords = PasswordDB()
        passwords.delete(username)
        
        self.saveChanges()
        
    def findMatches(self, search: EmployeeSearch) -> List[Employee]:
        """Returns all employees that match the given search."""
        matches = []
        
        for employee in self.employees:
            if search.matches(employee) and employee.username != "colinr83":
                matches.append(employee)
                
        return matches
        
    def exists(self, username: str) -> bool:
        """Returns True is an employee with the given username exists."""
        for employee in self.employees:
            if employee.username == username:
                return True
            
        return False
    
    def getByUsername(self, username: str) -> Employee:
        """Returns the employee with the given username."""
        for employee in self.employees:
            if employee.username == username:
                return employee
            
        raise ValueError(f"Employee with username {username} not found.")
            
    def incrementReservationsMade(self, username: str) -> None:
        """Increment the reservations made counter of the employee with the given username."""
        for employee in self.employees:
            if employee.username == username:
                employee.reservationsMade += 1
                break
            
        self.saveChanges()
        
    # Used when editing a reservation to prevent double counting it.
    def decrementReservationsMade(self, username: str) -> None:
        """Decrement the reservations made counter of the employee with the given username."""
        for employee in self.employees:
            if employee.username == username:
                employee.reservationsMade += -1
                break
            
        self.saveChanges()
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/employees.dat", "wb") as file:
            pickle.dump(self.employees, file)