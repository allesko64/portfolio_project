from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    predicted_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    predicted_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)