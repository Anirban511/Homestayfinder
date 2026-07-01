from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.place import PlaceOut


class BookingCreate(BaseModel):
    place_id: int
    check_in: datetime
    check_out: datetime
    guests: int = 1


class BookingOut(BaseModel):
    id: int
    place_id: int
    user_id: int
    check_in: datetime
    check_out: datetime
    guests: int
    price: float
    status: str
    payment_status: str
    place: PlaceOut | None = None

    model_config = ConfigDict(from_attributes=True)
