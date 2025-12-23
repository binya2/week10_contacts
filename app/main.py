import uvicorn
from fastapi import FastAPI

from app.routes import contacts

app = FastAPI(title="Rolling project")
app.include_router(contacts)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
