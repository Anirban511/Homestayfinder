from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PlaceCreate(BaseModel):
    title: str
    address: str
    description: str = ""
    price: float
    max_guests: int = 1
    photo: str = ""


class PlaceOut(BaseModel):
    id: int
    owner_id: int
    title: str
    address: str
    description: str
    price: float
    max_guests: int
    photo: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
