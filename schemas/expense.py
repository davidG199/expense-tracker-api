
import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class Expense(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=10, max_length=99)
    category: str = Field(min_length=2, max_length=50)
    date: datetime.datetime
    amount: float = Field(ge=1, le=1000000000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "description": "Description example for the expense",
                "category": "clothes",
                "date": "2012-04-21",
                "amount": 542212
            }
            ]
        }
    }


