from __future__ import annotations
from Reservation import Reservation

class ReservationSearch:
    def __init__(self, reservationID: int | None, customerID: int | None, employeeUser: str | None,
                 time: str | None, peopleNum: int | None) -> None:
        self.reservationID = reservationID
        self.customerID = customerID
        self.employeeUser = employeeUser
        self.time = time
        self.peopleNum = peopleNum
        
    def matches(self, reservation: Reservation) -> bool:
        if reservation.reservationID == self.reservationID:
            return True
        if reservation.customerID == self.customerID:
            return True
        if reservation.employeeUser == self.employeeUser:
            return True
        if reservation.time == self.time:
            return True
        if reservation.peopleNum == self.peopleNum:
            return True
        
        return False