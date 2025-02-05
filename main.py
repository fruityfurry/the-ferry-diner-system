# from Login import Login
# Login()  # Run login window. no need for mainloop as that is done in Login's __init__.

import AdminMenu
from EmployeeDB import EmployeeDB

employees = EmployeeDB()
user = employees.getByUsername("colinr83")  # Admin user.
AdminMenu.AdminMenu(user)  # Skip straight to admin menu. For testing purposes only.

# TODO: edit button on viewers which deletes then sends you to adder with fields prefilled? 