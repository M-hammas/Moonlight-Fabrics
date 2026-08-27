import json
from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate,ProductOut
from app.utils.dependencies import admin_user
router=APIRouter()
def out(p):
    d={c.name:getattr(p,c.name) for c in p.__table__.columns}
    for k in ("images","sizes","colors"):
        try:d[k]=json.loads(d.get(k) or "[]")
        except Exception:d[k]=[]
    return d
@router.get("",response_model=list[ProductOut])
def list_products(category:str|None=None,search:str|None=None,sale:bool|None=None,featured:bool|None=None,min_price:float|None=None,max_price:float|None=None,limit:int=Query(100,le=500),db:Session=Depends(get_db)):
    q=db.query(Product)
    if category:q=q.filter(Product.category.ilike(f"%{category.replace('-', ' ')}%"))
    if search:q=q.filter((Product.name.ilike(f"%{search}%"))|(Product.description.ilike(f"%{search}%")))
    if sale is not None:q=q.filter(Product.is_sale==sale)
    if featured is not None:q=q.filter(Product.featured==featured)
    if min_price is not None:q=q.filter(Product.price>=min_price)
    if max_price is not None:q=q.filter(Product.price<=max_price)
    return [out(p) for p in q.order_by(Product.featured.desc(),Product.id.desc()).limit(limit).all()]
@router.get("/{product_id}",response_model=ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p:raise HTTPException(404,"Product not found")
    return out(p)
@router.post("",response_model=ProductOut)
def create_product(payload:ProductCreate,db:Session=Depends(get_db),_=Depends(admin_user)):
    data=payload.model_dump();
    for k in ("images","sizes","colors"):data[k]=json.dumps(data[k])
    p=Product(**data);db.add(p);db.commit();db.refresh(p);return out(p)
@router.put("/{product_id}",response_model=ProductOut)
def update_product(product_id:int,payload:ProductCreate,db:Session=Depends(get_db),_=Depends(admin_user)):
    p=db.get(Product,product_id)
    if not p:raise HTTPException(404,"Product not found")
    data=payload.model_dump()
    for k in ("images","sizes","colors"):data[k]=json.dumps(data[k])
    for k,v in data.items():setattr(p,k,v)
    db.commit();db.refresh(p);return out(p)
@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),_=Depends(admin_user)):
    p=db.get(Product,product_id)
    if not p:raise HTTPException(404,"Product not found")
    db.delete(p);db.commit();return {"message":"Product deleted"}
