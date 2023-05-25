from fastapi import FastAPI

from .db import DB
from .router import user

app = FastAPI()
app.include_router(user.router)

# TODO: DB dependency


@app.get("/")
async def root():
    return {"message": "Hello World"}
