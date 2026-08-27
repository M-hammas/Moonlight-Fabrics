from pydantic import BaseModel,ConfigDict,Field
from decimal import Decimal
class ProductCreate(BaseModel):
    name:str
    slug:str
    sku:str|None=None
    category:str
    description:str=""
    price:Decimal
    sale_price:Decimal|None=None
    image:str=""
    images:list[str]=Field(default_factory=list)
    sizes:list[str]=Field(default_factory=list)
    colors:list[str]=Field(default_factory=list)
    stock:int=0
    rating:Decimal=0
    reviews:int=0
    is_new:bool=False
    is_sale:bool=False
    featured:bool=False
class ProductOut(BaseModel):
    id:int; name:str; slug:str; sku:str|None=None; category:str; description:str=""; price:Decimal; sale_price:Decimal|None=None; image:str=""; images:list[str]=Field(default_factory=list); sizes:list[str]=Field(default_factory=list); colors:list[str]=Field(default_factory=list); stock:int=0; rating:Decimal=0; reviews:int=0; is_new:bool=False; is_sale:bool=False; featured:bool=False
    model_config=ConfigDict(from_attributes=True)
