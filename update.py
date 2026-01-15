from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class updateuser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    number: Optional[str] = Field(
        default=None,
        pattern=r"^[6-9]\d{9}$"
    )
    role: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[int] = None


class updateproduct(BaseModel):
    Product_name:Optional [str] =None
    price:Optional [float] =None
    quantity:Optional [float]="none"
    description:Optional [str] =None
    date:Optional [str] =None
    
    