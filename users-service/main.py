from fastapi import FastAPI
from endpoints.authorization import router


app = FastAPI()

app.include_router(router, tags=["users"])


def main():
    pass