from Meal import Meal

class MealSearch:
    def __init__(self, nameSearch: str | None = None, price: float | None = None) -> None:
        self.nameSearch = nameSearch
        self.price = price
        
    def matches(self, meal: Meal) -> bool:
        if self.nameSearch is not None and meal.name.lower().find(self.nameSearch) == -1:
            return False
        if meal.price != self.price and self.price is not None:
            return False
        
        return True