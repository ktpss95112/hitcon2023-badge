from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI

from .db import connect_db
from .router import cardreader, crypto, dinorun, emoji, popcat, tap, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create DB before the app starts.
    """
    connect_db()
    yield
    # TODO: cleanup db


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(cardreader.router)
app.include_router(tap.router)
app.include_router(popcat.router)
app.include_router(dinorun.router)
app.include_router(emoji.router)
app.include_router(crypto.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/time")
async def get_time() -> datetime:
    return datetime.now()
