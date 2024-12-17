from dataclasses import dataclass

@dataclass
class Employee:
    username: str
    name: str
    reservationsMade: int