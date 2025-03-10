from Reservation import Reservation

class ReservationSearch:
    def __init__(self, reservationID: int | None = None, customerID: int | None = None, employeeUser: str | None = None,
                 time: str | None = None, peopleNum: int | None = None, customerSearch: str | None = None,
                 employeeSearch: str | None = None) -> None:
        """Reservation search class."""
        self.reservationID = reservationID
        self.customerID = customerID
        self.employeeUser = employeeUser
        self.time = time
        self.peopleNum = peopleNum
        self.customerSearch = customerSearch
        self.employeeSearch = employeeSearch
        
    def matches(self, reservation: Reservation) -> bool:
        """Returns True if the given reservation matches the search."""
        if self.reservationID is not None and reservation.reservationID != self.reservationID:
            return False
        if self.customerID is not None and reservation.customerID != self.customerID:
            return False
        if self.employeeUser is not None and reservation.employeeUser != self.employeeUser:
            return False
        if self.time is not None and reservation.time != self.time:
            return False
        if self.peopleNum is not None and reservation.peopleNum != self.peopleNum:
            return False
        
        return True