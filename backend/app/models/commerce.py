from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey, Text, func
from app.database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    title = Column(String(160), default="")
    body = Column(Text, default="")
    approved = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String(40), unique=True, index=True, nullable=False)
    kind = Column(String(20), default="percent", nullable=False)
    value = Column(Numeric(12,2), nullable=False)
    min_subtotal = Column(Numeric(12,2), default=0, nullable=False)
    max_uses = Column(Integer, nullable=True)
    uses = Column(Integer, default=0, nullable=False)
    active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(50), default="Home")
    recipient = Column(String(120), nullable=False)
    phone = Column(String(40), nullable=False)
    line1 = Column(String(300), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(30), default="")
    is_default = Column(Boolean, default=False)

class ReturnRequest(Base):
    __tablename__ = "return_requests"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(500), nullable=False)
    status = Column(String(30), default="requested", nullable=False)
    note = Column(String(500), default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(160), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(30), default="order")
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
