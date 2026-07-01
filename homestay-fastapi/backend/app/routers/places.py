from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Place, User
from app.schemas.place import PlaceCreate, PlaceOut

router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("", response_model=list[PlaceOut])
def list_places(db: Session = Depends(get_db)):
    return db.query(Place).order_by(Place.created_at.desc()).all()


# FEATURE: SEARCH — keyword across title/address/description + price/guest filters.
@router.get("/search", response_model=list[PlaceOut])
def search_places(
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    guests: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Place)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            Place.title.ilike(like),
            Place.address.ilike(like),
            Place.description.ilike(like),
        ))
    if min_price is not None:
        query = query.filter(Place.price >= min_price)
    if max_price is not None:
        query = query.filter(Place.price <= max_price)
    if guests is not None:
        query = query.filter(Place.max_guests >= guests)
    return query.order_by(Place.created_at.desc()).all()


@router.get("/{place_id}", response_model=PlaceOut)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.post("", response_model=PlaceOut, status_code=201)
def create_place(payload: PlaceCreate, db: Session = Depends(get_db),
                 current: User = Depends(get_current_user)):
    place = Place(owner_id=current.id, **payload.model_dump())
    db.add(place)
    db.commit()
    db.refresh(place)
    return place
