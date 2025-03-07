from dataclasses import dataclass

@dataclass
class Employee:
    """Employee class."""
    username: str
    name: str
    reservationsMade: int