import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from Reservation import Reservation

reservations = [
    Reservation(0, 2, "jasonizcool", "18:30", 2),
    Reservation(1, 0, "lauraaaa", "19:00", 1)
]

with open("data/reservations.dat", "wb+") as file:
    pickle.dump(reservations, file)