import pickle
from hashlib import sha256 as hash

username = "colinr83"
password = "ColinLovesBurgers369!"

passwordHashes = {
    username: int(hash(password.encode()).hexdigest(), 16)  # Hash password and convert to integer for storage.
}

with open("data/passwordHashes.dat", "wb+") as file:
    pickle.dump(passwordHashes, file)