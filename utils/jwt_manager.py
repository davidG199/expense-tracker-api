from jose import jwt
from fastapi import HTTPException

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_jwt
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")



