from dataclasses import dataclass

@dataclass
class Meal:
    mealID: int
    name: str
    price: float