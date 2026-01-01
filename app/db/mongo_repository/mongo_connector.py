import json
import os
from dataclasses import dataclass
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


@dataclass
class MongoConfig:
    """Configuration for MongoDB connection."""
    host: str = "localhost"
    port: int = 27017
    username: str = ""
    password: str = ""
    database: str = "PhonebookDB"


class MongoConnector:
    """MongoDB Connector Class"""

    def __init__(self, conf: MongoConfig):
        self._conf = conf
        self._client: Optional[MongoClient] = None
        self._db = None
        self._connect()

    def _connect(self):
        """Establishes a connection to the MongoDB server."""
        if self._conf.username and self._conf.password:
            uri = f"mongodb://{self._conf.username}:{self._conf.password}@{self._conf.host}:{self._conf.port}/"
        else:
            uri = f"mongodb://{self._conf.host}:{self._conf.port}/"
        try:
            self._client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self._client.admin.command('ping')
            self._db = self._client[self._conf.database]
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise e

    def get_db(self):
        """Returns the database instance."""
        if self._client is None:
            self._connect()
        return self._db

    def get_collection(self, collection_name: str):
        """Returns a specific collection from the database."""
        return self.get_db()[collection_name]

    def close(self):
        if self._client:
            self._client.close()


def init_db_from_json(conf: MongoConfig, file_path: str, collection_name: str) -> str:
    """Initializes the MongoDB database from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file: {file_path}")

    connector = MongoConnector(conf)
    db = connector.get_db()
    collection = db[collection_name]

    if collection.count_documents({}) > 0:
        connector.close()
        return conf.database
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            if data:
                collection.insert_many(data)
        elif isinstance(data, dict):
            collection.insert_one(data)
    except json.JSONDecodeError as e:
        raise e
    finally:
        connector.close()
    return conf.database
