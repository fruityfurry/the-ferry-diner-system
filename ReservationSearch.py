from __future__ import annotations
from Reservation import Reservation

class ReservationSearch:
    reservationID: int | None
    customerID: int | None
    employeeUser: str | None
    time: str | None
    peopleNum: int | None
    
    def __init__(self, reservationID: int | None, customerID: int | None, employeeUser: str | None,
                 time: str | None, peopleNum: int | None) -> None:
        self.reservationID = reservationID
        self.customerID = customerID
        self.employeeUser = employeeUser
        self.time = time
        self.peopleNum = peopleNum
        
    def matches(self, reservation: Reservation) -> bool:
        if 