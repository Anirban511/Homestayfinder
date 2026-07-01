from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Booking, Notification, Payment, User
from app.schemas.payment import PaymentConfirm, PaymentCreate, PaymentOut
from app.services.payment_service import payment_service

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.get("/config")
def config():
    return {"mode": payment_service.mode}


@router.post("/create-intent", response_model=PaymentOut)
def create_intent(payload: PaymentCreate, db: Session = Depends(get_db),
                  current: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current.id:
        raise HTTPException(status_code=403, detail="Not your booking")

    intent = payment_service.create_intent(booking.price, booking.id)
    payment = Payment(
        booking_id=booking.id, user_id=current.id, amount=booking.price,
        provider=intent["mode"], provider_ref=intent["provider_ref"],
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return PaymentOut(
        payment_id=payment.id, client_secret=intent["client_secret"],
        mode=intent["mode"], amount=booking.price,
    )


@router.post("/confirm")
def confirm(payload: PaymentConfirm, db: Session = Depends(get_db),
            current: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payload.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.user_id != current.id:
        raise HTTPException(status_code=403, detail="Not your payment")

    if not payment_service.confirm(payment.provider_ref):
        payment.status = "failed"
        db.commit()
        raise HTTPException(status_code=402, detail="Payment failed")

    payment.status = "succeeded"
    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    booking.payment_status = "paid"
    booking.status = "confirmed"
    db.add(Notification(
        user_id=current.id, type="payment",
        title="Payment successful", body="Your booking is confirmed.",
    ))
    db.commit()
    return {"ok": True}
