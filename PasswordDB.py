import pickle
from typing import Dict
from helpers import hash

class PasswordDB:
    def __init__(self) -> None:
        """Password database class. Create an instance of this class to interact with the database using its methods."""
        self.passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        
    def add(self, username: str, password: str) -> None:
        """Add a password associated with the given username to the database."""
        self.passwordHashes[username] = hash(password)  # Create entry in dictionary for given username and password.
        
        self.saveChanges()
        
    def delete(self, username: str) -> None:
        """Delete the password associated with the given username from the database."""
        self.passwordHashes.pop(username, None)  # Remove key from dictionary.
        
        self.saveChanges()
        
    def passwordIsCorrect(self, username: str, password: str) -> bool:
        """Returns True if the given password matches (hashes to the same value as) the password associated with
        the given username."""
        passwordHash = hash(password)
        
        # Assumes username exists. Validation is always done before this function is called.
        return self.passwordHashes[username] == passwordHash  # Returns true if password hashes to same value.
        
    def saveChanges(self) -> None:
        """Internal function. Saves changes to database."""
        with open("data/passwordHashes.dat", "wb") as file:
            pickle.dump(self.passwordHashes, file)