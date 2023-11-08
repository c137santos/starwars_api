import os
from pymongo import MongoClient

# Environment variables
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
MONGODB_USER = os.getenv("MONGODB_USER", "root")
MONGODB_PASS = os.getenv("MONGODB_PASS", "pass")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "starwars_db")


# MongoDB connection setup
class MongoDBConnection:
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = MongoClient(
                host=MONGODB_HOST,
                port=MONGODB_PORT,
                username=MONGODB_USER,
                password=MONGODB_PASS,
                authSource="admin",
            )
        return cls.client

    @classmethod
    def get_db(cls):
        return cls.get_client()[MONGODB_DB_NAME]

    @classmethod
    def films(cls):
        return cls.get_db().films

    @classmethod
    def planets(cls):
        return cls.get_db().planets
