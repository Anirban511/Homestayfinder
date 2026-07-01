from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Notification, User
from app.schemas.notification import NotificationList

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=NotificationList)
def list_notifications(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    items = (db.query(Notification)
             .filter(Notification.user_id == current.id)
             .order_by(Notification.created_at.desc()).limit(50).all())
    unread = (db.query(Notification)
              .filter(Notification.user_id == current.id, Notification.read == False)  # noqa: E712
              .count())
    return NotificationList(items=items, unread=unread)


@router.put("/read-all")
def read_all(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    (db.query(Notification)
     .filter(Notification.user_id == current.id, Notification.read == False)  # noqa: E712
     .update({Notification.read: True}))
    db.commit()
    return {"ok": True}
