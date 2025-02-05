from Meal import Meal

class MealSearch:
    def __init__(self, nameSearch: str | None = None, price: float | None = None) -> None:
        self.nameSearch = nameSearch
        self.price = price
        
    def matches(self, meal: Meal) -> bool:
        if self.nameSearch is not None and meal.name.lower().find(self.nameSearch.lower()) == -1:
            return False
        if self.price is not None and meal.price != self.price:
            return False
        
        return True