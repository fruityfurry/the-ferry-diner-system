# from Login import Login
# Login()  # Run login window. no need for mainloop as that is done in Login's __init__.

import AdminMenu
from Employee import Employee
from EmployeeDB import EmployeeDB
import pickle
from typing import List

employees = EmployeeDB()
user = employees.getByUsername("colinr83")  # Admin user.
AdminMenu.AdminMenu(user)  # Skip straight to admin menu. For testing purposes only.