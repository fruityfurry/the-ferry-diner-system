import pickle
from typing import Dict
from hashing import hash

class PasswordDB:
    def __init__(self) -> None:
        self.passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        
    def add(self, username: str, password: str) -> None:
        self.passwordHashes[username] = hash(password)  # Create entry in dictionary for given username and password.
        
        self.saveChanges()
        
    def delete(self, username: str) -> None:
        self.passwordHashes.pop(username, None)  # Remove key from dictionary.
        
        self.saveChanges()
        
    def passwordIsCorrect(self, username: str, password: str) -> bool:
        passwordHash = hash(password)
        
        # Assumes username exists. Validation is always done before this function is called.
        return self.passwordHashes[username] == passwordHash  # Returns true if password hashes to same value.
        
    def saveChanges(self) -> None:
        with open("data/passwordHashes.dat", "wb") as file:
            pickle.dump(self.passwordHashes, file)