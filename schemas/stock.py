from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    name: str
    symbol: str
    buy_price: Optional[float] = None
    quantity: Optional[int] = None
    purchase_date: Optional[str] = None
    user_id: Optional[int] = None


class StockCreate(StockBase):
    pass


class StockRead(StockBase):
    id: int

    class Config:
        from_attributes = True

