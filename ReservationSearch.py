from Reservation import Reservation
from CustomerDB import CustomerDB

class ReservationSearch:
    def __init__(self, reservationID: int | None = None, customerID: int | None = None, employeeUser: str | None = None,
                 time: str | None = None, peopleNum: int | None = None, customerSearch: str | None = None,
                 employeeSearch: str | None = None) -> None:
        self.reservationID = reservationID
        self.customerID = customerID
        self.employeeUser = employeeUser
        self.time = time
        self.peopleNum = peopleNum
        self.customerSearch = customerSearch
        self.employeeSearch = employeeSearch
        
    def matches(self, reservation: Reservation) -> bool:
        if reservation.reservationID != self.reservationID and self.reservationID is not None:
            return False
        if reservation.customerID != self.customerID and self.customerID is not None:
            return False
        if reservation.employeeUser != self.employeeUser and self.employeeUser is not None:
            return False
        if reservation.time != self.time and self.time is not None:
            return False
        if reservation.peopleNum != self.peopleNum and self.peopleNum is not None:
            return False
        
        return True