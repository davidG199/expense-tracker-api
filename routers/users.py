from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User
from config.database import Session
from services.user import UserService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.jwt_manager import create_access_token

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/", response_model=List[User], status_code=200)
def get_users() -> list:
    db = Session()
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@user_router.post("/new-user", response_model=dict, status_code=201)
def create_user(user: User) -> dict:
    db = Session()
    #verificamos si el email ya esta registrado
    email_user = UserService(db).get_user_by_email(user.email)
    if email_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    UserService(db).create_user(user)
    return JSONResponse(status_code=201, content={"message": "User created successfully"})

@user_router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = Session()
    user = UserService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}



