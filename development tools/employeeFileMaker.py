import pickle
from Employee import Employee

username = "colinr83"
name = "Colin Robinson"
reservationsMade = 2

with open("data/employees.dat", "wb+") as file:
    pickle.dump([Employee(username, name, reservationsMade)], file)
    