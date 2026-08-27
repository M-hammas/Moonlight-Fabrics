from sqlalchemy import Column,Integer,String,Boolean,DateTime,func
from app.database import Base
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String(120),nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    role=Column(String(30),default="customer",nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,server_default=func.now())
