from argon2 import PasswordHasher
import base64

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return ph.verify(hashed, password)

def encode_response(value:str)->str:
    return base64.urlsafe_b64encode(str(value).encode()).decode()


def decode_response(value:str)->str:
    return base64.urlsafe_b64decode(value.encode()).decode()
