
import re
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError("El username solo puede contener letras y números, sin espacios ni símbolos.")
        if len(value) < 3:
            raise ValueError("El username debe tener al menos 3 caracteres.")
        if len(value) > 20:
            raise ValueError("El username no puede tener más de 20 caracteres.")
        return value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[0-9]', value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("La contraseña debe contener al menos un carácter especial (!@#$%^&*...).")
        return value

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'example_user',
                    'email': 'example_email@example.com',
                    'password': 'ExamplePassword123!'
                }
            ]
        }
    }