from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.utils.dependencies import admin_user
router = APIRouter()
@router.get("/stats")
def stats(db: Session=Depends(get_db), _=Depends(admin_user)):
    revenue = db.query(func.coalesce(func.sum(Order.total), 0)).filter(Order.status != "cancelled").scalar()
    return {"customers": db.query(User).filter(User.role=="customer").count(), "products": db.query(Product).count(), "low_stock": db.query(Product).filter(Product.stock <= 5).count(), "orders": db.query(Order).count(), "pending_orders": db.query(Order).filter(Order.status.in_(["pending","confirmed","processing"])).count(), "revenue": float(revenue or 0)}
@router.get("/orders")
def orders(limit:int=100, db:Session=Depends(get_db), _=Depends(admin_user)):
    rows=db.query(Order).order_by(Order.id.desc()).limit(min(limit,500)).all()
    users={u.id:u for u in db.query(User).filter(User.id.in_([o.user_id for o in rows])).all()} if rows else {}
    return [{"id":o.id,"order_number":o.order_number,"status":o.status,"total":float(o.total or 0),"created_at":o.created_at.isoformat() if o.created_at else None,"user_id":o.user_id,"customer_name":users.get(o.user_id).name if users.get(o.user_id) else "—","customer_email":users.get(o.user_id).email if users.get(o.user_id) else "—","tracking_number":o.tracking_number,"courier":o.courier} for o in rows]
@router.get("/commerce")
def commerce(db:Session=Depends(get_db), _=Depends(admin_user)):
    return {"customers":db.query(User).filter(User.role=="customer").count(),"products":db.query(Product).count(),"orders":db.query(Order).count(),"revenue":float(db.query(func.coalesce(func.sum(Order.total),0)).filter(Order.status!="cancelled").scalar() or 0),"low_stock":db.query(Product).filter(Product.stock<=5).count()}
