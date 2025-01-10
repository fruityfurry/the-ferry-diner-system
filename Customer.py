from dataclasses import dataclass

@dataclass
class Customer:
    customerID: int
    fName: str
    sName: str
    phone: str