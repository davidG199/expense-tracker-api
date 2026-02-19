from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User
from config.database import get_db
from sqlalchemy.orm import Session
from services.user import UserService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.jwt_manager import create_access_token

user_router = APIRouter(prefix="/user", tags=["user"])

#endpoint para obtener todos los usuarios registrados, se devuelve una lista de usuarios en formato JSON
@user_router.get("/", response_model=List[User], status_code=200)
def get_users(db: Session = Depends(get_db)):
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#endpoint para crear un nuevo usuario, se verifica si el email ya esta registrado y se devuelve un mensaje de éxito o error en formato JSON
@user_router.post("/new-user", response_model=dict, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    #verificamos si el email ya esta registrado
    email_user = UserService(db).get_user_by_email(user.email)
    if email_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    UserService(db).create_user(user)
    return JSONResponse(status_code=201, content={"message": "User created successfully"})

#endpoint para login de usuario, se verifica si el email y contraseña son correctos y se devuelve un token de acceso en formato JSON
@user_router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = UserService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
    
#endpoint para eliminar un usuario por su id, se verifica si el usuario existe y se elimina, si no existe se devuelve un error 404
@user_router.delete("/delete-user/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = UserService(db).delete_user(user_id) #llamaos al método delete_user del servicio de usuario para eliminar el usuario por su id
    if not success:
        raise HTTPException(status_code=404, detail="User not found") #si el usuario no existe se devuelve un error 404
    return JSONResponse(status_code=200, content={"message": "User deleted successfully"}) #si el usuario se elimina correctamente se devuelve un mensaje de éxito



