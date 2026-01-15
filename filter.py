from pydantic import BaseModel, Field
from typing import Optional


class filterproduct(BaseModel):
    min_price:Optional [float]=None
    max_price:Optional [float]=None
    min_quantity:Optional [float]=None
    max_quantity:Optional [float]=None
    product_name:Optional [str]=None