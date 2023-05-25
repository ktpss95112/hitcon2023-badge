from fastapi import FastAPI
from .router import user
from .dependency import init_db

app = FastAPI()
app.include_router(user.router)

init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
