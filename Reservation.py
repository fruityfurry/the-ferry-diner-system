from dataclasses import dataclass

@dataclass
class Reservation:
    """Reservation class."""
    reservationID: int
    customerID: int
    employeeUser: str
    time: str
    peopleNum: int