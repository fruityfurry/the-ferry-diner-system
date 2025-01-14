import pickle
from typing import Dict
from hashing import hash

class PasswordDB:
    def __init__(self) -> None:
        self.passwordHashes: Dict[str, int] = pickle.load(open("data/passwordHashes.dat", "rb"))
        
    def add(self, username: str, password: str) -> None:
        self.passwordHashes[username] = hash(password)
        
        self.saveChanges()
        
    def delete(self, username: str) -> None:
        self.passwordHashes.pop(username, None)
        
        self.saveChanges()
        
    def passwordIsCorrect(self, username: str, password: str) -> bool:
        passwordHash = hash(password)
        
        return self.passwordHashes[username] == passwordHash
        
    def saveChanges(self) -> None:
        with open("data/passwordHashes.dat", "rb") as file:
            pickle.dump(self.passwordHashes, file)