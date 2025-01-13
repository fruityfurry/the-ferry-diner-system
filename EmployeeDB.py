import pickle
from typing import List, Dict
from Employee import Employee
from hashing import hash

class EmployeeDB:
    def __init__(self) -> None:
        self.employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
        
    def add(self, username: str, name: str, password: str) -> None:
        self.employees.append(Employee(username, name, 0))
        
        passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        passwordHashes[username] = hash(password)
        with open("data/passwordHashes.dat", "rb") as file:
            pickle.dump(passwordHashes, file)
            
        self.saveChanges()
    
    def delete(self, username: str) -> None:
        for employee in self.employees:
            if employee.username == username:
                self.employees.remove(employee)
                break
        
        self.saveChanges()
    
    def getByUsername(self, username: str) -> Employee:
        for employee in self.employees:
            if employee.username == username:
                return employee
            
        raise ValueError(f"Employee with usernam {username} was not found.")
            
    def incrementReservationsMade(self, username: str) -> None:
        for employee in self.employees:
            if employee.username == username:
                employee.reservationsMade += 1
                break
            
        self.saveChanges()
        
    def saveChanges(self) -> None:
        with open("data/employees.dat", "wb") as file:
            pickle.dump(self.employees, file)