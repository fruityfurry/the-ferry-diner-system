import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
import pprint
from Customer import Customer
from Employee import Employee
from Meal import Meal
from Reservation import Reservation

filepaths = [
    "data/customers.dat",
    "data/employees.dat",
    "data/meals.dat",
    "data/passwordHashes.dat",
    "data/reservations.dat",
    "data/timeslots.dat",
    "data/orders.dat"
]

for filepath in filepaths:
    data = pickle.load(open(filepath, "rb"))
    print(f"{filepath}: ")
    pprint.pprint(data, indent=2)
    print()