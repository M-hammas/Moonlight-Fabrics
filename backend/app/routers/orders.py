from decimal import Decimal
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.product import Product
from app.models.commerce import Coupon, Notification
from app.utils.dependencies import current_user, admin_user

router = APIRouter()
VALID_STATUSES = ("pending", "confirmed", "processing", "packed", "shipped", "out_for_delivery", "delivered", "cancelled")

class Item(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=50)

class OrderCreate(BaseModel):
    items: list[Item] = Field(min_length=1)
    shipping_address: str = Field(min_length=10, max_length=1000)
    phone: str = Field(min_length=7, max_length=40)
    payment_method: str = Field(default="cod")
    coupon_code: str = Field(default="", max_length=40)

def serialize_order(o, db):
    items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
    history = db.query(OrderStatusHistory).filter(OrderStatusHistory.order_id == o.id).order_by(OrderStatusHistory.id.asc()).all()
    return {
        "id": o.id, "order_number": o.order_number, "status": o.status,
        "payment_method": o.payment_method, "payment_status": o.payment_status,
        "subtotal": float(o.subtotal), "discount": float(o.discount or 0), "coupon_code": o.coupon_code,
        "shipping_fee": float(o.shipping_fee), "total": float(o.total), "shipping_address": o.shipping_address, "phone": o.phone,
        "tracking_number": o.tracking_number, "courier": o.courier,
        "created_at": o.created_at.isoformat() if o.created_at else None,
        "updated_at": o.updated_at.isoformat() if o.updated_at else None,
        "items": [{"id": i.id, "product_id": i.product_id, "product_name": i.product_name, "quantity": i.quantity, "unit_price": float(i.unit_price)} for i in items],
        "tracking": [{"status": h.status, "note": h.note, "created_at": h.created_at.isoformat() if h.created_at else None} for h in history],
    }

@router.post("")
def create_order(payload: OrderCreate, user=Depends(current_user), db: Session=Depends(get_db)):
    if payload.payment_method not in ("cod", "stripe"):
        raise HTTPException(400, "Unsupported payment method")
    product_ids = list({i.product_id for i in payload.items})
    products = {p.id: p for p in db.query(Product).filter(Product.id.in_(product_ids)).with_for_update().all()}
    subtotal = Decimal("0")
    checked = []
    for item in payload.items:
        p = products.get(item.product_id)
        if not p: raise HTTPException(404, f"Product {item.product_id} not found")
        if p.stock < item.quantity: raise HTTPException(409, f"Not enough stock for {p.name}")
        price = p.sale_price if p.sale_price is not None else p.price
        subtotal += price * item.quantity
        checked.append((p, item.quantity, price))
    discount = Decimal("0")
    coupon_code = payload.coupon_code.strip().upper()
    if coupon_code:
        from datetime import datetime
        coupon = db.query(Coupon).filter(Coupon.code == coupon_code, Coupon.active.is_(True)).with_for_update().first()
        if not coupon: raise HTTPException(400, "Invalid coupon")
        if coupon.expires_at and coupon.expires_at < datetime.utcnow(): raise HTTPException(400, "Coupon expired")
        if coupon.max_uses is not None and coupon.uses >= coupon.max_uses: raise HTTPException(400, "Coupon usage limit reached")
        if subtotal < coupon.min_subtotal: raise HTTPException(400, f"Minimum subtotal is PKR {coupon.min_subtotal}")
        discount = subtotal * coupon.value / Decimal("100") if coupon.kind == "percent" else coupon.value
        discount = min(discount, subtotal)
        coupon.uses += 1
    shipping = Decimal("0") if (subtotal - discount) >= Decimal("5000") else Decimal("250")
    total = subtotal - discount + shipping
    order = Order(
        order_number=f"SF-{uuid4().hex[:10].upper()}", user_id=user.id, status="confirmed",
        payment_method=payload.payment_method, payment_status="pending", subtotal=subtotal, discount=discount,
        coupon_code=coupon_code, shipping_fee=shipping, total=total, shipping_address=payload.shipping_address, phone=payload.phone,
        tracking_number=f"SFTRK-{uuid4().hex[:12].upper()}", courier="Sidra Fabrics Delivery"
    )
    db.add(order); db.flush()
    for p, qty, price in checked:
        p.stock -= qty
        db.add(OrderItem(order_id=order.id, product_id=p.id, product_name=p.name, quantity=qty, unit_price=price))
    db.add(OrderStatusHistory(order_id=order.id, status="confirmed", note="Order placed successfully"))
    db.add(Notification(user_id=user.id, title="Order confirmed", message=f"Your order {order.order_number} has been confirmed.", type="order"))
    db.commit(); db.refresh(order)
    return serialize_order(order, db)

@router.get("/my")
def my_orders(user=Depends(current_user), db: Session=Depends(get_db)):
    return [serialize_order(o, db) for o in db.query(Order).filter(Order.user_id == user.id).order_by(Order.id.desc()).all()]

# Specific routes MUST be declared before /{order_id}.
@router.get("/track/{order_number}")
def track_order(order_number: str, user=Depends(current_user), db: Session=Depends(get_db)):
    o = db.query(Order).filter(Order.order_number == order_number.strip().upper(), Order.user_id == user.id).first()
    if not o: raise HTTPException(404, "Order not found")
    return serialize_order(o, db)

@router.patch("/{order_id}/status")
def update_status(order_id: int, status: str = Query(...), note: str = Query(""), user=Depends(admin_user), db: Session=Depends(get_db)):
    if status not in VALID_STATUSES: raise HTTPException(400, "Invalid order status")
    o = db.get(Order, order_id)
    if not o: raise HTTPException(404, "Order not found")
    if o.status == "delivered" and status != "delivered": raise HTTPException(409, "Delivered orders cannot move backwards")
    if o.status == "cancelled" and status != "cancelled": raise HTTPException(409, "Cancelled orders cannot be reopened")
    previous_status = o.status
    o.status = status
    if status == "cancelled" and previous_status != "cancelled":
        for item in db.query(OrderItem).filter(OrderItem.order_id == o.id).all():
            product = db.get(Product, item.product_id)
            if product: product.stock += item.quantity
    if status == "delivered": o.payment_status = "paid"
    db.add(OrderStatusHistory(order_id=o.id, status=status, note=note or f"Order marked {status.replace('_',' ')}"))
    db.add(Notification(user_id=o.user_id, title="Order update", message=f"{o.order_number}: {status.replace('_',' ')}", type="order"))
    db.commit(); db.refresh(o)
    return serialize_order(o, db)

@router.get("/{order_id}")
def get_order(order_id: int, user=Depends(current_user), db: Session=Depends(get_db)):
    o = db.get(Order, order_id)
    if not o or o.user_id != user.id: raise HTTPException(404, "Order not found")
    return serialize_order(o, db)
