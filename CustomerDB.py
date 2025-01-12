import pickle
from typing import List
from Customer import Customer

class CustomerDB:
    def __init__(self) -> None:
        self.customers: List[Customer] = pickle.load(open("data/customers.dat", "rb"))
        
    def add(self, fName: str, sName: str, phone: str) -> None:
        customerID = self.customers[-1].customerID + 1
        
        self.customers.append(Customer(customerID, fName, sName, phone))
        
        self.saveChanges()
        
    def saveChanges(self) -> None:
        with open("data/customers.dat", "wb") as file:
            pickle.dump(self.customers, file)