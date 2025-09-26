import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()


uri = os.getenv("Mongo_DB_url")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)