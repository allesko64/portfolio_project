from database import DatabaseManager
from models.users import users
from models.stocks import stocks
from models.prediction import prediction
from models.chat_history import chat_history

if __name__ == "__main__":
    db = DatabaseManager()

    user_model = users()
    stock_model = stocks()
    prediction_model = prediction()
    chat_model = chat_history()

    # Create all tables
    user_model.create()
    stock_model.create_table()
    prediction_model.create_table()
    chat_model.create_table()

    # Example usage
    user_model.insert("ayush", "ayush@example.com")

    db.close()
