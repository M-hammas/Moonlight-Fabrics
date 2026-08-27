from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import SECRET_KEY

oauth2=OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def current_user(token:str=Depends(oauth2),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        uid=int(payload["sub"])
    except (JWTError,KeyError,ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    user=db.get(User,uid)
    if not user: raise HTTPException(status_code=401,detail="User not found")
    return user

def admin_user(user=Depends(current_user)):
    if user.role!="admin": raise HTTPException(status_code=403,detail="Admin access required")
    return user
