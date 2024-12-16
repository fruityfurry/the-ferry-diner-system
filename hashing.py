from hashlib import sha256

def hash(text: str) -> int:
    textBytes = text.encode()
    hashNumHex = sha256(textBytes).hexdigest()
    hashNum = int(hashNumHex, 16)
    return hashNum