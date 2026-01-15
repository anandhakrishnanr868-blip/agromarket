from pydantic import BaseModel,EmailStr,Field,field_validator


class product(BaseModel):
    Product_name:str
    price:float
    quantity:float
    description:str
    date:str
    image_url:str
    user_id:str