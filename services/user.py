from models.user import User as UserModel
from schemas.user import User

class UserService():

    def __init__(self, db) -> None:
        self.db = db

    def get_users(self):
        result = self.db.query(UserModel).all()
        return result
    
    def create_user(self, user: User):
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        return new_user

    #buscamos a un usuario segun su email
    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def authenticate_user(self, email: str, password: str):
        email = self.get_user_by_email(email)
        passw = self.db.query(UserModel).filter(UserModel.password == password).first() 
        if not email and not passw:
            return False
        return email
        



