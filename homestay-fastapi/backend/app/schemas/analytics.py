from pydantic import BaseModel


class AdminStats(BaseModel):
    users: int
    places: int
    bookings: int
    revenue: float


class PricePoint(BaseModel):
    label: str
    value: float


class AnalyticsOut(BaseModel):
    stats: AdminStats
    bookings_by_status: list[PricePoint]
    revenue_by_day: list[PricePoint]
