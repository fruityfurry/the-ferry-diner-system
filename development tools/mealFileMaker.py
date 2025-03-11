import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from Meal import Meal


meals = [
    Meal(0, "Steamed Oysters", 14.99),
    Meal(1, "Cheeseboard", 6.99),
    Meal(2, "Scrambled Eggs", 6.99),
    Meal(3, "Tomato Soup", 8.99),
    Meal(4, "Fresh Scampi and Chips", 11.99)
]

with open("data/meals.dat", "wb+") as file:
    pickle.dump(meals, file)