
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WishlistItem, Product
from app.utils.dependencies import current_user
router=APIRouter()
@router.get("")
def list_wishlist(user=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.query(WishlistItem,Product).join(Product,Product.id==WishlistItem.product_id).filter(WishlistItem.user_id==user.id).all()
    return [{"id":p.id,"name":p.name,"price":float(p.price),"sale_price":float(p.sale_price) if p.sale_price is not None else None,"image":p.image,"stock":p.stock} for _,p in rows]
@router.post("/{product_id}")
def add(product_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    if not db.get(Product,product_id): return {"ok":False,"message":"Product not found"}
    if not db.query(WishlistItem).filter_by(user_id=user.id,product_id=product_id).first():
        db.add(WishlistItem(user_id=user.id,product_id=product_id));db.commit()
    return {"ok":True}
@router.delete("/{product_id}")
def remove(product_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    row=db.query(WishlistItem).filter_by(user_id=user.id,product_id=product_id).first()
    if row:db.delete(row);db.commit()
    return {"ok":True}
