from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from security import decode_response

class product(BaseModel):
    Product_name: str
    price: float
    quantity: float
    description: Optional[str] = None
    date: str
    user_id: str
    image: str

    @field_validator("user_id")
    @classmethod
    def decode_user_id(cls, value: str) -> str:
        return decode_response(value)
