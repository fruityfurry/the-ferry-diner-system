import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
import pickle
from Order import Order

orders = []

with open("data/orders.dat", "wb+") as file:
    pickle.dump(orders, file)