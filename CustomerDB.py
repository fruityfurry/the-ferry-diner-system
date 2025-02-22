import pickle
from typing import List
from Customer import Customer
from CustomerSearch import CustomerSearch
import ReservationDB
from binarySearch import binarySearch

# There are exceptions raised here for some failure cases but they will never run as the parameters passed into all
# these functions are thoroughly validated. 

class CustomerDB:
    def __init__(self) -> None:
        self.customers: List[Customer] = pickle.load(open("data/customers.dat", "rb"))
        
    def add(self, fName: str, sName: str, phone: str) -> None:
        if len(self.customers) == 0:
            customerID = 0
        else:
            customerID = self.customers[-1].customerID + 1
        
        self.customers.append(Customer(customerID, fName, sName, phone))
        
        self.saveChanges()
        
    def delete(self, customerID: int) -> None:
        index = binarySearch(self.customers, customerID, lambda x: x.customerID)
        
        if index == -1: raise ValueError(f"Customer with ID {customerID} was not found.")
                                         
        del self.customers[index]
            
        reservations = ReservationDB.ReservationDB()
        reservations.deleteAssociated(customerID)
            
        self.saveChanges()
        
    def exists(self, fName: str, sName: str, phone: str) -> bool:
        for customer in self.customers:
            if (customer.fName == fName and
                customer.sName == sName and
                customer.phone == phone):
                return True
            
        return False
    
    def findMatches(self, search: CustomerSearch) -> List[Customer]:
        matches = []
        
        for customer in self.customers:
            if search.matches(customer):
                matches.append(customer)
                
        return matches
    
    def getID(self, fName: str, sName: str, phone: str) -> int:
        for customer in self.customers:
            if (customer.fName == fName and
                customer.sName == sName and
                customer.phone == phone):
                return customer.customerID
        
        raise ValueError(f"Customer {fName} {sName} (Phone: {phone}) was not found.")
    
    def getByID(self, customerID: int) -> Customer:
        index = binarySearch(self.customers, customerID, lambda x: x.customerID)
        
        if index == -1: raise ValueError(f"Customer with ID {customerID} was not found.")
    
        return self.customers[index]
        
    def saveChanges(self) -> None:
        with open("data/customers.dat", "wb") as file:
            pickle.dump(self.customers, file)