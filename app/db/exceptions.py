"""Custom exceptions for database operations in the application."""
class AppDatabaseError(Exception):
    pass

class RecordNotFound(AppDatabaseError):
    pass

class OperationFailed(AppDatabaseError):
    pass