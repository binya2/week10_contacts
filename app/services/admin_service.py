from db import reload_db

class AdminService:
    def reload_system_config(self):
        reload_db()
        return True