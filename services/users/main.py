import uvicorn
from alembic import command
from alembic.config import Config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from endpoints.authorization import router
from core.db import init_db, session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    await session_manager.close()


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

app.include_router(router, tags=["users"], prefix="/users")


def main():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)


if __name__ == "__main__":
    main()