import pickle
from typing import List
from Employee import Employee
from PasswordDB import PasswordDB
from EmployeeSearch import EmployeeSearch

class EmployeeDB:
    def __init__(self) -> None:
        self.employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
        
    def add(self, username: str, name: str, password: str) -> None:
        self.employees.append(Employee(username, name, 0))
        
        passwords = PasswordDB()
        passwords.add(username, password)
            
        self.saveChanges()
    
    def delete(self, username: str) -> None:
        for employee in self.employees:
            if employee.username == username:
                self.employees.remove(employee)
                break
            
        print(self.employees)
            
        passwords = PasswordDB()
        passwords.delete(username)
        
        self.saveChanges()
        
    def findMatches(self, search: EmployeeSearch) -> List[Employee]:
        matches = []
        
        for employee in self.employees:
            if search.matches(employee) and employee.username != "colinr83":
                matches.append(employee)
                
        return matches
        
    def exists(self, username: str) -> bool:
        for employee in self.employees:
            if employee.username == username:
                return True
            
        return False
    
    def getByUsername(self, username: str) -> Employee:
        for employee in self.employees:
            if employee.username == username:
                return employee
            
        raise ValueError(f"Employee with username {username} was not found.")
            
    def incrementReservationsMade(self, username: str) -> None:
        for employee in self.employees:
            if employee.username == username:
                employee.reservationsMade += 1
                break
            
        self.saveChanges()
        
    # Used when editing a reservation to prevent double counting it.
    def decrementReservationsMade(self, username: str) -> None:
        for employee in self.employees:
            if employee.username == username:
                employee.reservationsMade += -1
                break
            
        self.saveChanges()
        
    def saveChanges(self) -> None:
        with open("data/employees.dat", "wb") as file:
            pickle.dump(self.employees, file)