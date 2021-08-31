from pymongo import MongoClient
from src.config import conf

class Database:
    def __init__(self, db_name="politweet"):
        self.client = MongoClient(conf['mongo_uri'])
        self.db = self.client[db_name]

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
