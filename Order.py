from dataclasses import dataclass

@dataclass
class Order:
    """Order class."""
    orderID: int
    reservationID: int
    mealID: int