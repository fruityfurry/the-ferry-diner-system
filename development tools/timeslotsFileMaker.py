import pickle

timeslots = [
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30"
]

with open("data/timeslots.dat", "wb+") as file:
    pickle.dump(timeslots, file)