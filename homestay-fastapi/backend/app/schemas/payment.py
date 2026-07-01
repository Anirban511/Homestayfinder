from pydantic import BaseModel


class PaymentCreate(BaseModel):
    booking_id: int


class PaymentOut(BaseModel):
    payment_id: int
    client_secret: str
    mode: str
    amount: float


class PaymentConfirm(BaseModel):
    payment_id: int
