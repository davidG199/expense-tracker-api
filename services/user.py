import bcrypt
from models.user import User as UserModel
from schemas.user import User
from sqlalchemy.orm import Session

class UserService():

    def __init__(self, db: Session) -> None:
        self.db = db

    #funcion para obtener los usuarios
    def get_users(self):
        result = self.db.query(UserModel).all()
        return result
    
    #funcion para crear un usuario
    def create_user(self, user: User):

        #hash de la contraseña antes de guardar usuario
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        #se crea el usuario con la contraseña hasheada
        user_data = user.model_dump()
        user_data['password'] = hashed_password.decode('utf-8')
        new_user = UserModel(**user_data)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    #buscamos a un usuario segun su email
    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    #autenticamos al usuario comparando la contraseña ingresada con la contraseña hasheada en la base de datos
    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email)
        if not user:
            return False
        
        if not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            return False

        return user
        
    #obtener un usuario por su id
    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    #Eliminar usuario por su id
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True


