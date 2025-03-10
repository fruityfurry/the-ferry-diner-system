import pickle
from typing import List
from Customer import Customer
from CustomerSearch import CustomerSearch
import ReservationDB
from helpers import binarySearch

class CustomerDB:
    def __init__(self) -> None:
        """Customer database class. Create an instance of this class to interact with the database using its methods."""
        self.customers: List[Customer] = pickle.load(open("data/customers.dat", "rb"))
        
    # Add a customer to the database.
    def add(self, fName: str, sName: str, phone: str) -> None:
        """Add a customer with the given details."""
        # Generate a unique customerID.
        if len(self.customers) == 0:
            customerID = 0
        else:
            customerID = self.customers[-1].customerID + 1
        
        # Add customer to database.
        self.customers.append(Customer(customerID, fName, sName, phone))
        
        self.saveChanges()
        
    def delete(self, customerID: int) -> None:
        """Delete a customer with the given ID."""
        # Find index of customer to be deleted. Entries are PK ascending so binary search can be used.
        index = binarySearch(self.customers, customerID, lambda x: x.customerID)
        
        if index == -1: raise ValueError(f"Customer with customerID {customerID} not found.")
                                  
        # Remove customer from database.       
        del self.customers[index]
            
        # Delete the customer's reservations so tehy aren't left orphaned.
        reservations = ReservationDB.ReservationDB()
        reservations.deleteAssociated(customerID)
            
        self.saveChanges()
        
    def exists(self, fName: str, sName: str, phone: str) -> bool:
        """Returns True if a customer with the given details exists."""
        # Linear search for customer.
        for customer in self.customers:
            if (customer.fName == fName and
                customer.sName == sName and
                customer.phone == phone):
                return True
            
        return False
    
    def findMatches(self, search: CustomerSearch) -> List[Customer]:
        """Returns all customers that match the given search."""
        matches = []
        
        # Iterate over all customers and add them to match list if they match.
        for customer in self.customers:
            if search.matches(customer):
                matches.append(customer)
                
        return matches
    
    def getID(self, fName: str, sName: str, phone: str) -> int:
        """Returns the ID of a customer with the given details."""
        # Linearly search through all customers to find match.
        for customer in self.customers:
            if (customer.fName == fName and
                customer.sName == sName and
                customer.phone == phone):
                return customer.customerID
        
        raise ValueError(f"Customer named {fName} {sName} with phone number {phone} not found.")
    
    def getByID(self, customerID: int) -> Customer:
        """Returns the customer that has the given ID."""
        # Find index of customer. Entries are PK ascending so binary search can be used.
        index = binarySearch(self.customers, customerID, lambda x: x.customerID)
        
        if index == -1: raise ValueError(f"Customer with customerID {customerID} not found.")
    
        return self.customers[index]
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/customers.dat", "wb") as file:
            pickle.dump(self.customers, file)