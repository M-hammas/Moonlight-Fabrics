from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, Text
from app.database import Base
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_number = Column(String(32), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(40), default="pending", nullable=False, index=True)
    payment_method = Column(String(30), default="cod", nullable=False)
    payment_status = Column(String(30), default="pending", nullable=False)
    subtotal = Column(Numeric(12,2), default=0, nullable=False)
    shipping_fee = Column(Numeric(12,2), default=0, nullable=False)
    discount = Column(Numeric(12,2), default=0, nullable=False)
    coupon_code = Column(String(40), default="")
    total = Column(Numeric(12,2), default=0, nullable=False)
    shipping_address = Column(Text, default="", nullable=False)
    phone = Column(String(40), default="", nullable=False)
    tracking_number = Column(String(64), unique=True, index=True, nullable=True)
    courier = Column(String(120), default="Sidra Fabrics Delivery")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(40), nullable=False)
    note = Column(String(500), default="")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
