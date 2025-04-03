import uvicorn
from alembic import command
from alembic.config import Config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from endpoints.authorization import router
from core.db import init_db, session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await session_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["users"])


def main():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)