import pickle
from hashing import hash

# Password and corresponding username to write to file.
username = "colinr83"
password = "ColinLovesBurger$369"

passwordHashes = {
    username: hash(password)  # Hash password and convert to integer for storage.
}

# Write to file.
with open("data/passwordHashes.dat", "wb+") as file:
    pickle.dump(passwordHashes, file)