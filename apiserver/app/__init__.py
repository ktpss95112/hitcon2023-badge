from fastapi import FastAPI
from .router import user, cardreader, tap
from .db import init_db

app = FastAPI()
app.include_router(user.router)
app.include_router(cardreader.router)
app.include_router(tap.router)

init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
