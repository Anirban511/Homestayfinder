from fastapi import APIRouter, Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Message, Notification, User
from app.schemas.message import MessageCreate, MessageOut

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post("", response_model=MessageOut, status_code=201)
def send_message(payload: MessageCreate, db: Session = Depends(get_db),
                 current: User = Depends(get_current_user)):
    msg = Message(
        sender_id=current.id, recipient_id=payload.recipient_id,
        place_id=payload.place_id, text=payload.text,
    )
    db.add(msg)
    db.add(Notification(
        user_id=payload.recipient_id, type="message",
        title=f"New message from {current.name}",
        body=payload.text[:60],
    ))
    db.commit()
    db.refresh(msg)
    return msg


# Thread of messages between the current user and another user.
@router.get("/{other_id}", response_model=list[MessageOut])
def thread(other_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    msgs = (db.query(Message).filter(or_(
        and_(Message.sender_id == current.id, Message.recipient_id == other_id),
        and_(Message.sender_id == other_id, Message.recipient_id == current.id),
    )).order_by(Message.created_at.asc()).all())
    return msgs
