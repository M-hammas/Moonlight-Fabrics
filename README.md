# Sidra Fabrics Ecommerce — Professional V5

A full-stack Pakistani fashion e-commerce application with React/Vite, FastAPI, PostgreSQL, JWT authentication, server-side stock validation, COD checkout, Stripe-ready payments, admin fulfillment controls, live order-status tracking and responsive motion design.

## Important V5 fixes

- Fixed the Docker **Failed to fetch** problem: the browser now uses the Nginx `/api` reverse proxy in the full Docker stack.
- Fixed the PostgreSQL driver mismatch (`psycopg`, not `psycopg2`).
- Fixed the order tracking route collision where `/orders/track/...` could be captured by `/{order_id}`.
- Added persistent tracking number + courier fields and a full customer tracking timeline.
- Added admin order-status controls that update the customer's tracking history.
- Added safe cancellation inventory restoration and prevented reopening cancelled orders.
- Added startup demo seeding for Docker development.
- Added real external product photography URLs with local-image migration/fallback handling.
- Added stronger loading/error/network handling and session validation.
- Added premium entrance, hover, image, floating, tracking and mobile animations.
- Removed random homepage sorting so the UI remains stable and predictable.

## Run with Docker — recommended

1. Start Docker Desktop.
2. From this project folder run:

```bash
docker compose up --build
```

Or double-click `start-full-stack.bat` on Windows.

Open:

```text
http://localhost
```

The Docker stack contains:

- React/Vite storefront
- Nginx SPA + `/api` reverse proxy
- FastAPI backend
- PostgreSQL 16
- Automatic development seed data

### Development admin

```text
Email: admin@sidra-fabrics.local
Password: Admin@12345
```

Change this before any public deployment.

## Run without Docker

### Backend

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Create `backend/.env` from `backend/.env.example`, point `DATABASE_URL` at a running PostgreSQL database, then:

```bash
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

### Frontend

In another terminal:

```bash
npm install
npm run dev
```

For local Vite development, use:

```text
VITE_API_URL=http://localhost:8000/api
```

## Real commerce notes

The order system is database-backed: prices and stock are revalidated on the server when an order is created. Admin status changes create persistent tracking-history records that the customer tracking page reads from the API.

Cash on Delivery works without a payment-provider account. Stripe checkout is implemented but requires your own Stripe secret/webhook credentials before card payments can be accepted.

The tracking number in this development build is an internal Sidra Fabrics tracking reference. It is not a live courier GPS/parcel API. For production courier tracking, connect your actual courier provider's API and replace the generated reference with the provider's tracking number.

Before public launch, also configure HTTPS, a production secret key, production CORS origins, real legal/return policies, Stripe keys, courier integration, transactional email/SMS, backups and monitoring.
