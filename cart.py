from pydantic import BaseModel,Field


class addcart(BaseModel):
    user_id:str
    product_id:str



