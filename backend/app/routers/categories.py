
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
router=APIRouter()
@router.get("")
def list_categories(db:Session=Depends(get_db)):
    return [{"id":c.id,"name":c.name,"slug":c.slug,"image":c.image} for c in db.query(Category).order_by(Category.name).all()]
