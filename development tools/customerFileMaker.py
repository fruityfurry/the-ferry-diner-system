import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
import pickle
from Customer import Customer

customers = [
    Customer(0, "Sam", "Mawdsley", "07837898832"),
    Customer(1, "Reece", "Baker", "07345473772"),
    Customer(2, "Tom", "Dave", "07625633390"),
    Customer(3, "Kenneth", "Taylor", "07622911108"),
    Customer(4, "Adam", "Lock-it", "07262822918"),
    Customer(5, "Carly", "Gomery", "07724822276"),
    Customer(6, "Wren", "Butler", "07837299319")
]

with open("data/customers.dat", "wb+") as file:
    pickle.dump(customers, file)