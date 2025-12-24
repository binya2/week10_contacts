import json
import os
from pathlib import Path
from typing import Dict, Any

from .manager import DatabaseManager


def _load_raw_settings() -> tuple[Any, dict[Any, Any] | Any]:
    settings = {}
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config.json"

    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                data = json.load(f)
                active = data.get("active_db", "mysql")
                if active in data.get("connections", {}):
                    settings = data["connections"][active]
        except Exception:
            pass

    return active, settings


def get_db_manager() -> DatabaseManager:
    db_type, raw_settings = _load_raw_settings()
    print(db_type, raw_settings)
    if db_type == "mysql":
        from .sql_repository import create_sql_db_manager
        return create_sql_db_manager(raw_settings)

    elif db_type == "mongo":
        # from .mongo_repository import create_mongo_db_manager
        # return create_mongo_db_manager(raw_settings)
        raise NotImplementedError("Mongo not implemented yet")

    else:
        raise ValueError(f"Unknown DB Type: {db_type}")

