from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User as UserModel
from config.database import Session
from utils.jwt_manager import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

load_dotenv()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        db = Session()
        user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
        db.close()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user 
    except Exception as e:
        raise HTTPException(status_code=401, detail={"Invalid token": str(e)})


