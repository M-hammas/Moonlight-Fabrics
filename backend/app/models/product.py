from sqlalchemy import Column,Integer,String,Numeric,Boolean,Text
from app.database import Base
class Product(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True)
    name=Column(String(255),nullable=False)
    slug=Column(String(255),unique=True,index=True,nullable=False)
    sku=Column(String(80),unique=True,index=True,nullable=True)
    category=Column(String(100),index=True,nullable=False)
    description=Column(Text,default="")
    price=Column(Numeric(12,2),nullable=False)
    sale_price=Column(Numeric(12,2),nullable=True)
    image=Column(String(1000),default="")
    images=Column(Text,default="[]")
    sizes=Column(Text,default="[]")
    colors=Column(Text,default="[]")
    stock=Column(Integer,default=0)
    rating=Column(Numeric(3,2),default=0)
    reviews=Column(Integer,default=0)
    is_new=Column(Boolean,default=False)
    is_sale=Column(Boolean,default=False)
    featured=Column(Boolean,default=False)
