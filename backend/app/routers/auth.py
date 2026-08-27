from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest,LoginRequest
from app.utils.security import hash_password,verify_password,create_access_token
from app.utils.dependencies import current_user
router=APIRouter()

@router.post("/register")
def register(payload:RegisterRequest,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==payload.email).first():
        raise HTTPException(409,"Email already registered")
    user=User(name=payload.name,email=payload.email,password_hash=hash_password(payload.password))
    db.add(user);db.commit();db.refresh(user)
    return {"access_token":create_access_token(user.id),"token_type":"bearer","user":{"id":user.id,"name":user.name,"email":user.email,"role":user.role}}

@router.post("/login")
def login(payload:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email).first()
    if not user or not verify_password(payload.password,user.password_hash):
        raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_access_token(user.id),"token_type":"bearer","user":{"id":user.id,"name":user.name,"email":user.email,"role":user.role}}

@router.get("/me")
def me(user=Depends(current_user)):
    return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}
