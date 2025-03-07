from dataclasses import dataclass

@dataclass
class Customer:
    """Customer class."""
    customerID: int
    fName: str
    sName: str
    phone: str