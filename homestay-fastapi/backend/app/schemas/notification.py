from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificationOut(BaseModel):
    id: int
    type: str
    title: str
    body: str
    read: bool
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class NotificationList(BaseModel):
    items: list[NotificationOut]
    unread: int
