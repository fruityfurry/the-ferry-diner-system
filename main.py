from Login import Login
Login()  # Run login window. no need for mainloop as that is done in Login's __init__.

# from Windows import AdminMenu
# from Windows import ReservationMaker
# from Employee import Employee
# import pickle
# from typing import List

# employees: List[Employee] = pickle.load(open("data/employees.dat", "rb"))
# user = employees[0]  # Admin user.
# ReservationMaker(user)  # Skip straight to admin menu. For testing purposes only.