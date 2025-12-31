import os
from pathlib import Path

from .mongo_connector import MongoConnector, MongoConfig, init_db_from_json
from .repositories.contact_mongo import MongoContactRepository
from .. import DatabaseManager


def create_mongo_db_manager(settings: dict) -> DatabaseManager:
    if os.getenv("MONGO_HOST"): settings["host"] = os.getenv("MONGO_HOST")
    if os.getenv("MONGO_USER"): settings["username"] = os.getenv("MONGO_USER")
    if os.getenv("MONGO_PASSWORD"): settings["password"] = os.getenv("MONGO_PASSWORD")

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
