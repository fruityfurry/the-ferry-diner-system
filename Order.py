from dataclasses import dataclass

@dataclass
class Order:
    orderID: int
    reservationID: int
    mealID: int