from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Booking, Notification, Place, User
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db),
                   current: User = Depends(get_current_user)):
    place = db.query(Place).filter(Place.id == payload.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    nights = max(1, (payload.check_out - payload.check_in).days)
    booking = Booking(
        place_id=place.id, user_id=current.id,
        check_in=payload.check_in, check_out=payload.check_out,
        guests=payload.guests, price=nights * place.price,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Notify the host of the new booking request.
    db.add(Notification(
        user_id=place.owner_id, type="booking",
        title="New booking request",
        body=f'{current.name} requested to book "{place.title}".',
    ))
    db.commit()
    return booking


# FEATURE: HISTORY — the current user's bookings.
@router.get("", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return (db.query(Booking)
            .filter(Booking.user_id == current.id)
            .order_by(Booking.created_at.desc()).all())
