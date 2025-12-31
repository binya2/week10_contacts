from db import reload_db

class AdminService:

    @classmethod
    def reload_system_config(cls):
        """Reloads the database configuration from config.json."""
        reload_db()
        return True