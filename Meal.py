from dataclasses import dataclass

@dataclass
class Meal:
    """Meal class."""
    mealID: int
    name: str
    price: float