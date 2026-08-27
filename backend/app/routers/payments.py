import os
from fastapi import APIRouter,Depends,HTTPException,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order
from app.models.commerce import Notification
from app.utils.dependencies import current_user
router=APIRouter()
@router.post('/stripe/checkout/{order_id}')
def stripe_checkout(order_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    o=db.get(Order,order_id)
    if not o or o.user_id!=user.id: raise HTTPException(404,'Order not found')
    if o.payment_method!='stripe': raise HTTPException(400,'Order is not a Stripe order')
    key=os.getenv('STRIPE_SECRET_KEY')
    if not key: raise HTTPException(503,'Stripe is not configured. Add STRIPE_SECRET_KEY to backend environment.')
    import stripe
    stripe.api_key=key
    session=stripe.checkout.Session.create(mode='payment',line_items=[{'price_data':{'currency':'pkr','product_data':{'name':f'Sidra Fabrics {o.order_number}'},'unit_amount':int(o.total*100)},'quantity':1}],success_url=os.getenv('STRIPE_SUCCESS_URL','http://localhost:5173/order-success?payment=success'),cancel_url=os.getenv('STRIPE_CANCEL_URL','http://localhost:5173/checkout?payment=cancelled'),metadata={'order_id':str(o.id),'order_number':o.order_number})
    return {'checkout_url':session.url,'session_id':session.id}
@router.post('/stripe/webhook')
async def stripe_webhook(request:Request,db:Session=Depends(get_db)):
    payload=await request.body(); signature=request.headers.get('stripe-signature'); secret=os.getenv('STRIPE_WEBHOOK_SECRET')
    try:
        import stripe
        if secret:
            event=stripe.Webhook.construct_event(payload,signature,secret)
        else:
            import json; event=json.loads(payload)
    except Exception as exc: raise HTTPException(400,f'Invalid webhook: {exc}')
    if event.get('type') in ('checkout.session.completed','checkout.session.async_payment_succeeded'):
        session=event['data']['object']; oid=(session.get('metadata') or {}).get('order_id')
        if oid:
            o=db.get(Order,int(oid))
            if o:
                o.payment_status='paid'; db.add(Notification(user_id=o.user_id,title='Payment received',message=f'Payment confirmed for {o.order_number}.',type='payment')); db.commit()
    return {'received':True}
