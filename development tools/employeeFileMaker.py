import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
import pickle
from Employee import Employee

with open("data/employees.dat", "wb+") as file:
    pickle.dump([Employee("colinr83", "Colin Robinson", 0),
                 Employee("jasonizcool", "Jason Mendoza", 0),
                 Employee("lauraaaa", "Laura Stockton", 0)], file)