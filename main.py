from Login import Login

# Login()  # Run login window. no need for mainloop as that is done in Login's __init__.

from AdminMenu import AdminMenu
from Employee import Employee
import pickle
from typing import List

employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
user = employees[0]  # Admin user.
AdminMenu(user)  # Skip straight to admin menu. For testing purposes ONLY.