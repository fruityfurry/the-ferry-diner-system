import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
import pickle
from Employee import Employee

username = "colinr83"
name = "Colin Robinson"
reservationsMade = 2

with open("data/employees.dat", "wb+") as file:
    pickle.dump([Employee(username, name, reservationsMade)], file)