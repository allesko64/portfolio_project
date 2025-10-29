from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.decorators import log_call , time_execution
from database import Base, engine, get_db
from models.stocks import Stock
from models.users import User

app = FastAPI()

# Create tables if they don't exist yet (simple bootstrapping)
Base.metadata.create_all(bind=engine)

@app.get("/ping")
def ping():
    return {"status" : "ok"}




@app.get("/portfolio")
@log_call
def list_portfolio(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
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