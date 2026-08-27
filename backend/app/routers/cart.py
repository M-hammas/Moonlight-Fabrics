
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.utils.dependencies import current_user
router=APIRouter()
@router.get("")
def cart_info(user=Depends(current_user),db:Session=Depends(get_db)):
    return {"user_id":user.id,"items":[],"message":"Cart is managed client-side until checkout; server validates stock and prices."}
