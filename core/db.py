from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ MongoDB Error:", e)

db = client["bnpl_app"]

users_col = db["users"]
info_col = db["information"]
predict_col = db["predict"]