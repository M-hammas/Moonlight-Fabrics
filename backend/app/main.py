import os
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app import models
from app.migrate import ensure_columns
from app.routers import auth, products, orders, categories, cart, wishlist, reviews, admin, commerce, payments
app=FastAPI(title="Sidra Fabrics Ecommerce API",version="4.0.0",docs_url="/docs",redoc_url="/redoc")
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.middleware("http")
async def security_headers(request:Request,call_next):
    response=await call_next(request)
    response.headers["X-Content-Type-Options"]="nosniff"; response.headers["X-Frame-Options"]="DENY"; response.headers["Referrer-Policy"]="strict-origin-when-cross-origin"; response.headers["Permissions-Policy"]="camera=(), microphone=(), geolocation=()"
    return response
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine); ensure_columns(engine)
    if os.getenv("SEED_DEMO_DATA", "false").lower() == "true":
        from app.seed import seed_demo
        seed_demo()
for router,prefix,tags in [(auth.router,"/api/auth",["Authentication"]),(products.router,"/api/products",["Products"]),(orders.router,"/api/orders",["Orders"]),(categories.router,"/api/categories",["Categories"]),(cart.router,"/api/cart",["Cart"]),(wishlist.router,"/api/wishlist",["Wishlist"]),(reviews.router,"/api/reviews",["Reviews"]),(admin.router,"/api/admin",["Admin"]),(commerce.router,"/api/commerce",["Commerce"]),(payments.router,"/api/payments",["Payments"])]:app.include_router(router,prefix=prefix,tags=tags)
@app.get("/")
def root():return {"service":"sidra-fabrics-api","version":"4.0.0","status":"ok"}
@app.get("/api/health")
def health():return {"status":"ok","service":"sidra-fabrics-api","version":"4.0.0"}
@app.exception_handler(Exception)
async def unhandled(request:Request,exc:Exception):
    # Keep internal errors out of client responses; details stay in server logs under normal Uvicorn logging.
    return JSONResponse(status_code=500,content={"detail":"Internal server error"})
