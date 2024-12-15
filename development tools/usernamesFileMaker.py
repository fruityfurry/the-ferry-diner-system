import pickle

usernames = ["colinr83"]

with open("data/usernames.dat", "wb+") as file:
    pickle.dump(usernames, file)
    