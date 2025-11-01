from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.decorators import log_call , time_execution
from app.database import Base, engine, get_db
from models.stocks import Stock
from models.users import User
from models.chat_history import ChatHistory

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
async def ping():
    return {"status" : "ok"}




@app.get("/portfolio")
@log_call
async def list_portfolio(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stock))
    stocks = result.scalars().all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "symbol": s.symbol,
            "buy_price": s.buy_price,
            "quantity": s.quantity,
            "purchase_date": s.purchase_date.isoformat() if s.purchase_date else None,
            "user_id": s.user_id,
        }
        for s in stocks
    ]