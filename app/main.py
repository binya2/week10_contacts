import uvicorn
from fastapi import FastAPI

from routes import admin
from routes import contacts_api

app = FastAPI(title="Rolling project")
app.include_router(contacts_api)
app.include_router(admin)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True,
    )
