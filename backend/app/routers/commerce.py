from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WishlistItem, Review, Coupon, Address, ReturnRequest, Notification, Product, Order
from app.utils.dependencies import current_user, admin_user

router = APIRouter()

class WishlistPayload(BaseModel): product_id: int
class ReviewPayload(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    title: str = Field(default="", max_length=160)
    body: str = Field(default="", max_length=2000)
class CouponPayload(BaseModel): code: str
class AddressPayload(BaseModel):
    label: str = "Home"; recipient: str; phone: str; line1: str; city: str; postal_code: str = ""; is_default: bool = False
class ReturnPayload(BaseModel): order_id: int; reason: str = Field(min_length=5, max_length=500)

@router.get("/wishlist")
def wishlist(user=Depends(current_user), db: Session=Depends(get_db)):
    rows=db.query(WishlistItem,Product).join(Product,Product.id==WishlistItem.product_id).filter(WishlistItem.user_id==user.id).order_by(WishlistItem.id.desc()).all()
    return [{"id":w.id,"product":{"id":p.id,"name":p.name,"price":float(p.price),"sale_price":float(p.sale_price) if p.sale_price is not None else None,"image":p.image,"stock":p.stock,"rating":float(p.rating or 0)}} for w,p in rows]

@router.post("/wishlist")
def add_wishlist(payload: WishlistPayload,user=Depends(current_user),db: Session=Depends(get_db)):
    if not db.get(Product,payload.product_id): raise HTTPException(404,"Product not found")
    if not db.query(WishlistItem).filter_by(user_id=user.id,product_id=payload.product_id).first(): db.add(WishlistItem(user_id=user.id,product_id=payload.product_id)); db.commit()
    return {"ok":True}

@router.delete("/wishlist/{product_id}")
def remove_wishlist(product_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    row=db.query(WishlistItem).filter_by(user_id=user.id,product_id=product_id).first()
    if row: db.delete(row); db.commit()
    return {"ok":True}

@router.get("/reviews/{product_id}")
def reviews(product_id:int,db:Session=Depends(get_db)):
    rows=db.query(Review).filter_by(product_id=product_id,approved=True).order_by(Review.id.desc()).all()
    return [{"id":r.id,"rating":r.rating,"title":r.title,"body":r.body,"created_at":r.created_at.isoformat() if r.created_at else None} for r in rows]

@router.post("/reviews")
def add_review(payload:ReviewPayload,user=Depends(current_user),db:Session=Depends(get_db)):
    p=db.get(Product,payload.product_id)
    if not p: raise HTTPException(404,"Product not found")
    existing=db.query(Review).filter_by(user_id=user.id,product_id=p.id).first()
    if existing: raise HTTPException(409,"You already reviewed this product")
    r=Review(user_id=user.id,product_id=p.id,rating=payload.rating,title=payload.title,body=payload.body)
    db.add(r); db.flush()
    approved=db.query(Review).filter_by(product_id=p.id,approved=True).all()
    p.reviews=len(approved); p.rating=Decimal(sum(x.rating for x in approved))/Decimal(len(approved))
    db.commit(); return {"ok":True,"review_id":r.id}

@router.post("/coupons/validate")
def validate_coupon(payload:CouponPayload, subtotal:float, db:Session=Depends(get_db)):
    c=db.query(Coupon).filter(Coupon.code==payload.code.strip().upper(),Coupon.active==True).first()
    if not c: raise HTTPException(404,"Invalid coupon")
    if c.expires_at and c.expires_at < datetime.utcnow(): raise HTTPException(400,"Coupon expired")
    if c.max_uses is not None and c.uses>=c.max_uses: raise HTTPException(400,"Coupon usage limit reached")
    if Decimal(str(subtotal)) < c.min_subtotal: raise HTTPException(400,f"Minimum subtotal is PKR {c.min_subtotal}")
    discount=(Decimal(str(subtotal))*c.value/100) if c.kind=="percent" else c.value
    discount=min(discount,Decimal(str(subtotal)))
    return {"code":c.code,"kind":c.kind,"value":float(c.value),"discount":float(discount),"total_after_discount":float(Decimal(str(subtotal))-discount)}

@router.get("/addresses")
def addresses(user=Depends(current_user),db:Session=Depends(get_db)):
    return [{"id":a.id,"label":a.label,"recipient":a.recipient,"phone":a.phone,"line1":a.line1,"city":a.city,"postal_code":a.postal_code,"is_default":a.is_default} for a in db.query(Address).filter_by(user_id=user.id).order_by(Address.is_default.desc(),Address.id.desc()).all()]

@router.post("/addresses")
def add_address(payload:AddressPayload,user=Depends(current_user),db:Session=Depends(get_db)):
    if payload.is_default: db.query(Address).filter_by(user_id=user.id).update({"is_default":False})
    a=Address(user_id=user.id,**payload.model_dump()); db.add(a); db.commit(); db.refresh(a); return {"id":a.id,"label":a.label,"recipient":a.recipient,"phone":a.phone,"line1":a.line1,"city":a.city,"postal_code":a.postal_code,"is_default":a.is_default}

@router.get("/notifications")
def notifications(user=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.query(Notification).filter_by(user_id=user.id).order_by(Notification.id.desc()).limit(50).all()
    return [{"id":n.id,"title":n.title,"message":n.message,"type":n.type,"read":n.read,"created_at":n.created_at.isoformat() if n.created_at else None} for n in rows]

@router.patch("/notifications/{notification_id}/read")
def mark_notification(notification_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    n=db.query(Notification).filter_by(id=notification_id,user_id=user.id).first()
    if not n: raise HTTPException(404,"Notification not found")
    n.read=True; db.commit(); return {"ok":True}

@router.post("/returns")
def request_return(payload:ReturnPayload,user=Depends(current_user),db:Session=Depends(get_db)):
    o=db.get(Order,payload.order_id)
    if not o or o.user_id!=user.id: raise HTTPException(404,"Order not found")
    if o.status not in ("delivered",): raise HTTPException(400,"Returns can be requested after delivery")
    existing=db.query(ReturnRequest).filter_by(order_id=o.id,user_id=user.id).first()
    if existing: raise HTTPException(409,"Return already requested")
    r=ReturnRequest(order_id=o.id,user_id=user.id,reason=payload.reason); db.add(r); db.add(Notification(user_id=user.id,title="Return request received",message=f"Return request for {o.order_number} is under review.",type="return")); db.commit(); return {"ok":True,"return_id":r.id,"status":r.status}

@router.get("/returns")
def my_returns(user=Depends(current_user),db:Session=Depends(get_db)):
    return [{"id":r.id,"order_id":r.order_id,"reason":r.reason,"status":r.status,"note":r.note,"created_at":r.created_at.isoformat() if r.created_at else None} for r in db.query(ReturnRequest).filter_by(user_id=user.id).order_by(ReturnRequest.id.desc()).all()]

@router.get("/admin/returns")
def admin_returns(user=Depends(admin_user),db:Session=Depends(get_db)):
    return [{"id":r.id,"order_id":r.order_id,"user_id":r.user_id,"reason":r.reason,"status":r.status,"note":r.note} for r in db.query(ReturnRequest).order_by(ReturnRequest.id.desc()).all()]

@router.patch("/admin/returns/{return_id}")
def update_return(return_id:int,status:str,user=Depends(admin_user),db:Session=Depends(get_db)):
    if status not in ("requested","approved","rejected","refunded","received"): raise HTTPException(400,"Invalid return status")
    r=db.get(ReturnRequest,return_id)
    if not r: raise HTTPException(404,"Return not found")
    r.status=status; db.add(Notification(user_id=r.user_id,title="Return updated",message=f"Your return request is now {status}.",type="return")); db.commit(); return {"ok":True,"status":status}

@router.post("/admin/coupons")
def create_coupon(payload:dict,user=Depends(admin_user),db:Session=Depends(get_db)):
    code=str(payload.get("code","")).strip().upper()
    if not code: raise HTTPException(400,"Coupon code required")
    if db.query(Coupon).filter_by(code=code).first(): raise HTTPException(409,"Coupon already exists")
    c=Coupon(code=code,kind=payload.get("kind","percent"),value=Decimal(str(payload.get("value",0))),min_subtotal=Decimal(str(payload.get("min_subtotal",0))),max_uses=payload.get("max_uses"),expires_at=datetime.fromisoformat(payload["expires_at"]) if payload.get("expires_at") else None)
    db.add(c); db.commit(); db.refresh(c); return {"id":c.id,"code":c.code}
