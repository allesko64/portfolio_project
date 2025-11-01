from fastapi import FastAPI, Depends,HTTPException,Response,responses,status
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)



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








