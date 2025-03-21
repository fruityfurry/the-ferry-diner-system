import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from Employee import Employee

with open("data/employees.dat", "wb+") as file:
    pickle.dump([Employee("colinr83", "Colin Robinson", 0),
                 Employee("jasonizcool", "Jason Mendoza", 1),
                 Employee("lauraaaa", "Laura Stockton", 1)], file)