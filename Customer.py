from dataclasses import dataclass

# Customer class.
@dataclass
class Customer:
    customerID: int
    fName: str
    sName: str
    phone: str