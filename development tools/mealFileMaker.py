import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
import pickle
from Meal import Meal


meals = [
    Meal(0, "Steamed Oysters", 14.99),
    Meal(1, "Cheeseboard", 12.99),
    Meal(2, "Scrambled Eggs", 6.99)
]

with open("data/meals.dat", "wb+") as file:
    pickle.dump(meals, file)