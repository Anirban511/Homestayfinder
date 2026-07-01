from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_admin
from app.models import Booking, Payment, Place, User
from app.schemas.analytics import AdminStats, AnalyticsOut, PricePoint
from app.schemas.auth import UserOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
def stats(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    revenue = (db.query(Payment).filter(Payment.status == "succeeded").all())
    return AdminStats(
        users=db.query(User).count(),
        places=db.query(Place).count(),
        bookings=db.query(Booking).count(),
        revenue=sum(p.amount for p in revenue),
    )


# FEATURE: ANALYTICS — aggregates for the charts on the analytics page.
@router.get("/analytics", response_model=AnalyticsOut)
def analytics(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    bookings = db.query(Booking).all()
    by_status: dict[str, int] = defaultdict(int)
    by_day: dict[str, float] = defaultdict(float)
    for b in bookings:
        by_status[b.status] += 1
        if b.payment_status == "paid" and b.created_at:
            by_day[b.created_at.strftime("%Y-%m-%d")] += b.price

    payments = db.query(Payment).filter(Payment.status == "succeeded").all()
    stats_obj = AdminStats(
        users=db.query(User).count(),
        places=db.query(Place).count(),
        bookings=len(bookings),
        revenue=sum(p.amount for p in payments),
    )
    return AnalyticsOut(
        stats=stats_obj,
        bookings_by_status=[PricePoint(label=k, value=v) for k, v in by_status.items()],
        revenue_by_day=[PricePoint(label=k, value=v) for k, v in sorted(by_day.items())],
    )


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(User).order_by(User.created_at.desc()).all()
