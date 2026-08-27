from datetime import datetime,timedelta,timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM="HS256"
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password): return pwd.hash(password)
def verify_password(password,hashed): return pwd.verify(password,hashed)
def create_access_token(subject):
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub":str(subject),"exp":expire},SECRET_KEY,algorithm=ALGORITHM)
