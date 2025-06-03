from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["uzchat_ai"]
category_collection = db["categories"]
qa_collection = db["qa"]
