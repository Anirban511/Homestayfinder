from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False, index=True)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    max_guests = Column(Integer, default=1)
    photo = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="places")
    bookings = relationship("Booking", back_populates="place")
