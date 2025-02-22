# import Login
# Login.Login()  # Run login window. no need for mainloop as that is done in Login's __init__.
#                # This same technique is used for all windows in this program.

import AdminMenu
from EmployeeDB import EmployeeDB

employees = EmployeeDB()
user = employees.getByUsername("colinr83")  # Admin user.
AdminMenu.AdminMenu(user)  # Skip straight to admin menu. For testing purposes only.