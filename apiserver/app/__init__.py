from datetime import datetime

from fastapi import FastAPI

from .db import init_db
from .router import cardreader, popcat, tap, user

app = FastAPI()
app.include_router(user.router)
app.include_router(cardreader.router)
app.include_router(tap.router)
app.include_router(popcat.router)

init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/time")
async def get_time() -> datetime:
    return datetime.now()
