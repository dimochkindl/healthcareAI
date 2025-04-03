import os
import load_dotenv

load_dotenv.load_dotenv(".env")


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
ENVIRONMENT = os.getenv("ENVIRONMENT")
ALGORITHM = os.getenv("ENV_ALGORITHM")
ACCESS_SECRET_KEY = os.getenv("ENV_ACCESS_SECRET_KEY")

GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
SYSTEM_PROMPT = "Ты помощник врача. После каждого ответа добавляй что-то в духе 'Вам стоит обратиться к врачу для получения проффесиональнай помощи' "
