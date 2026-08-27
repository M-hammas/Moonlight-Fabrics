from fastapi import APIRouter
router=APIRouter()
@router.get("")
def reviews_health(): return {"status":"ready","resource":"reviews","use":"/api/commerce/reviews/{product_id}"}
