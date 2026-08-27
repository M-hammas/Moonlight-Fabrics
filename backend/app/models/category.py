from sqlalchemy import Column,Integer,String
from app.database import Base
class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True)
    name=Column(String(120),unique=True,nullable=False)
    slug=Column(String(120),unique=True,index=True,nullable=False)
    image=Column(String(1000),default="")
