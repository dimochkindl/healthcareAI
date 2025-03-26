import uvicorn
from alembic import command
from alembic.config import Config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from endpoints.authorization import router


app = FastAPI()

app.include_router(router, tags=["users"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    pass


def main():
    alembic_cfg = Config("./alembic.ini")
    command.upgrade(alembic_cfg, "head")
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)