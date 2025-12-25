from db import reload_db

class AdminService:

    @classmethod
    def reload_system_config(cls):
        reload_db()
        return True