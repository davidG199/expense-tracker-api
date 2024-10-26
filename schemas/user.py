
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(min_length=2, max_length=50)
    email:str = Field(min_length=4, max_length=99)
    password: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'example_user',
                    'email': 'example_email@example.com',
                    'password': 'example_password'
                }
            ]
        }
    }