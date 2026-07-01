from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, func

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    provider = Column(String, default="stub")
    provider_ref = Column(String, default="")
    status = Column(String, default="created")  # created|succeeded|failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
