import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from helpers import hash

# Password and corresponding username to write to file.
username = "colinr83"
password = "ColinLovesBurger$369"

passwordHashes = {
    username: hash(password)  # Hash password and convert to integer for storage.
}

# Write to file.
with open("data/passwordHashes.dat", "wb+") as file:
    pickle.dump(passwordHashes, file)