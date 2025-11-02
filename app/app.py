from fastapi import FastAPI, Depends,HTTPException,Response,responses,status
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from utils.decorators import log_call , time_execution
from app.database import Base, engine, get_db
from models.stocks import Stock
from models.users import User
from models.chat_history import ChatHistory
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError 
from models.users import User
from schemas.user import UserCreate, UserRead
from typing import List
from models.stocks import Stock
from schemas.stock import StockCreate, StockRead




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is managed by Alembic migrations.
    # No runtime table creation here.
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    await db.refresh(db_user)
    return db_user


@app.get("/api/users", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users   
    


@app.get("/api/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int ,db:AsyncSession=Depends(get_db)):
    user = await db.get(User,user_id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.put("/api/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int , payload:UserCreate,db:AsyncSession=Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    user.username = payload.username
    user.email = payload.email
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int ,db:AsyncSession=Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    await db.delete(user)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/api/stocks",response_model=StockRead,status_code=status.HTTP_201_CREATED)
async def create_stock(stock: StockCreate,db: AsyncSession = Depends(get_db)):
    db_stock = Stock(name=stock.name, symbol=stock.symbol, buy_price=stock.buy_price, quantity=stock.quantity, purchase_date=stock.purchase_date, user_id=stock.user_id)
    db.add(db_stock)
    await db.commit()
    await db.refresh(db_stock)
    return db_stock

@app.get("/api/stocks",response_model=List[StockRead])
async def list_stocks(db: AsyncSession = Depends(get_db)):
    stmt = select(Stock)
    result = await db.execute(stmt)
    stocks = result.scalars().all()
    return stocks


@app.get("/api/stocks/{stock_id}",response_model=StockRead)
async def get_stock(stock_id: int , db:AsyncSession=Depends(get_db)):
    stock = await db.get(Stock ,stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock

@app.put("/api/stocks/{stock_id}",response_model=StockRead)
async def update_stock(stock_id: int , payload:StockCreate,db:AsyncSession=Depends(get_db)):
    stock = await db.get(Stock ,stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    stock.name = payload.name
    stock.symbol = payload.symbol
    stock.buy_price = payload.buy_price
    stock.quantity = payload.quantity
    stock.purchase_date = payload.purchase_date
    await db.commit()
    await db.refresh(stock)
    return stock

@app.delete("/api/stocks/{stock_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(stock_id: int ,db:AsyncSession=Depends(get_db)):
    stock = await db.get(Stock ,stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    await db.delete(stock)
    await db.commit()



