import uvicorn
from alembic.config import Config
from alembic import command
from core.db import database
from core.http import create_response
from endpoints import business_logic
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from urllib3.exceptions import InsecureRequestWarning


app = FastAPI(title="AI Chat Bot API")
app.include_router(router=business_logic.router, prefix="/business", tags=["business"])


@app.exception_handler(InsecureRequestWarning)
async def response_exception_handler(request:Request, exc: InsecureRequestWarning):
	return JSONResponse(
		status_code=401,
		content=await create_response(message=f'Insecure request on {request.headers}', code=401),
	)


@app.on_event("startup")
async def startup():
	await database.connect()


@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()


if __name__ == "__main__":
	alembic_cfg = Config("./alembic.ini")
	command.upgrade(alembic_cfg, "head")
	uvicorn.run("main:app", port=8006, host="0.0.0.0", reload=True)
