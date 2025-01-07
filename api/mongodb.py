from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://mquan592003:p8dHF9UXgCKxygbC@bibabibum203-db.pucog.mongodb.net/?retryWrites=true&w=majority&appName=bibabibum203-db")
    return client["NMCNPM"]