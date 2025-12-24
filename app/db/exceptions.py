class AppDatabaseError(Exception):
    pass

class RecordNotFound(AppDatabaseError):
    pass

class OperationFailed(AppDatabaseError):
    pass