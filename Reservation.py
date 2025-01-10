from dataclasses import dataclass

@dataclass
class Reservation:
    reservationID: int
    customerID: int
    employeeUser: str
    time: str
    peopleNum: int