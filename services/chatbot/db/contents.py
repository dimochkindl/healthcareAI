import sqlalchemy
from pgvector.sqlalchemy import Vector
from core.db import metadata


contents = sqlalchemy.Table(
    "contents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("text", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("embedding", Vector(1024), nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=True, default=sqlalchemy.func.now()),
)
