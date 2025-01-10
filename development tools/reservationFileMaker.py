import pickle

reservations = []

with open("data/reservations.dat", "wb+") as file:
    pickle.dump(reservations, file)