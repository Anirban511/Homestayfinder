from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    recipient_id: int
    text: str
    place_id: int | None = None


class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    place_id: int | None = None
    text: str
    read: bool
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
