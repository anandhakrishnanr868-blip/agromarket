from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import Optional


class product(BaseModel):
    Product_name: str
    price: float
    quantity: float
    description: Optional[str] = None
    date: str
    user_id: str
    image: str 
