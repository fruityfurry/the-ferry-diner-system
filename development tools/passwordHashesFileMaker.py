import sys
sys.path.insert(1, "C:/Users/kasss/Documents/My Code/Python/The Ferry Diner")  # Allows import of files in parent directory.
# This is an absolute file path, so it won't work on anyone's system but mine. This is fine though since this is just
# a development tool.
import pickle
from helpers import hash

passwordHashes = {
    "colinr83": hash("ColinLovesBurger$369"),  # Hash password and convert to integer for storage.
    "jasonizcool": hash("Jason123!"),
    "lauraaaa": hash("MyPasswordIsLongerThanYourPassword2005!")
}

# Write to file.
with open("data/passwordHashes.dat", "wb+") as file:
    pickle.dump(passwordHashes, file)