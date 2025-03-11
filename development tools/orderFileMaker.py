import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from Order import Order

orders = [
    Order(0, 0, 1, 1),
    Order(0, 0, 2, 2),
    Order(0, 1, 3, 1)
]

with open("data/orders.dat", "wb+") as file:
    pickle.dump(orders, file)