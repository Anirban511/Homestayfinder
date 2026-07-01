"""FastAPI application entrypoint: CORS, rate limiting, router wiring."""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.rate_limit import rate_limiter
from app.routers import admin, auth, bookings, messages, notifications, payments, places

# Create tables on startup (for production, use Alembic migrations instead).
import app.models  # noqa: F401  (ensures models are registered on Base)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HomestayFinder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    # Vercel generates a unique preview URL per branch/PR (e.g.
    # homestayfinder-git-feature-x-yourname.vercel.app). This regex allows any
    # preview deployment of the project without listing each one explicitly.
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "payment_mode": settings.PAYMENT_MODE}


# Rate limiting is applied to all routers as a shared dependency.
limited = [Depends(rate_limiter)]
app.include_router(auth.router, dependencies=limited)
app.include_router(places.router, dependencies=limited)
app.include_router(bookings.router, dependencies=limited)
app.include_router(payments.router, dependencies=limited)
app.include_router(notifications.router, dependencies=limited)
app.include_router(messages.router, dependencies=limited)
app.include_router(admin.router, dependencies=limited)
