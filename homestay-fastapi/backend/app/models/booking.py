from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    guests = Column(Integer, default=1)
    price = Column(Float, default=0)
    status = Column(String, default="pending")          # pending|confirmed|cancelled
    payment_status = Column(String, default="unpaid")    # unpaid|paid|refunded
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    place = relationship("Place", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
