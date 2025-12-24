import os

import uvicorn
from fastapi import FastAPI

from routes import admin
from routes import contacts_api

app = FastAPI(title="Rolling project")
app.include_router(contacts_api)
app.include_router(admin)

if __name__ == "__main__":
    app_port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=app_port,
        reload=True,
    )
