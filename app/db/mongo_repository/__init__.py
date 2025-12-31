import os
from pathlib import Path

from db.manager import DatabaseManager

from .mongo_connector import MongoConnector, MongoConfig, init_db_from_json
from .repositories.contact_mongo import MongoContactRepository


def create_mongo_db_manager(settings: dict) -> DatabaseManager:
    """Creates and returns a DatabaseManager for MongoDB."""
    if os.getenv("MONGO_HOST"): settings["host"] = os.getenv("MONGO_HOST")
    if os.getenv("MONGO_PORT"): settings["port"] = int(os.getenv("MONGO_PORT"))
    if os.getenv("MONGO_DB"): settings["database"] = os.getenv("MONGO_DB")

    if os.getenv("DB_USER"): settings["username"] = os.getenv("DB_USER")
    if os.getenv("DB_PASSWORD"): settings["password"] = os.getenv("DB_PASSWORD")

    conf = MongoConfig(**settings)

    try:
        base_dir = Path(__file__).resolve().parent
        json_path = base_dir / "init.json"
        real_db_name = init_db_from_json(conf, str(json_path), collection_name="contacts")
        conf.database = real_db_name
    except Exception as e:
        print(f"Bootstrap Warning: {e}")

    connector = MongoConnector(conf)

    return DatabaseManager(contacts=MongoContactRepository(connector), _connector=connector)


__all__ = ["MongoConnector", "MongoContactRepository", "create_mongo_db_manager"]
