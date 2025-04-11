import logging
from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from core.config import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PORT, POSTGRES_PASSWORD, POSTGRES_DB
from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager


logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_sessionmaker] = None

    def init(self, host: str):
        db_url = (
            f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
        )
        print("db_url", db_url)

        pool_class = NullPool if 'test' in host else None

        self._engine = create_async_engine(
            db_url,
            echo=True,
            pool_size=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_timeout=30,
            connect_args={
                "command_timeout": 60,
                'server_settings': {
                    'application_name': 'users',
                    'jit': 'off'
                }
            },
            poolclass=pool_class,
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False,
            class_=AsyncSession,
        )

    async def close(self):
        if self._engine is None:
            raise SQLAlchemyError('DatabaseSessionManager is not initialized')

        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
        if self._engine is None:
            raise SQLAlchemyError('DatabaseSessionManager is not initialized')

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                print(f'Exception while connecting to database: {e}')
                await conn.rollback()
                raise

    @asynccontextmanager
    async def manage_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._session_maker is None:
            raise SQLAlchemyError('DatabaseSessionManager is not initialized')

        single_session = self._session_maker()
        try:
            yield single_session
        except Exception as e:
            print(f'Exception while connecting to database: {e}')
            await single_session.rollback()
            raise
        finally:
            await single_session.close()

    async def create_all(self, connection: Optional[AsyncConnection] = None):
        if not connection:
            async with self.connect() as conn:
                await conn.run_sync(DefaultBase.metadata.create_all)
        else:
            await connection.run_sync(DefaultBase.metadata.create_all)

    async def drop_all(self, connection: Optional[AsyncConnection] = None):
        if not connection:
            async with self.connect() as conn:
                await conn.run_sync(DefaultBase.metadata.drop_all)
        else:
            await connection.run_sync(DefaultBase.metadata.drop_all)


session_manager = DatabaseSessionManager()

def init_db():
    session_manager.init(POSTGRES_HOST)
    logger.info('Database initialized')

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.manage_session() as session:
        yield session


async def manage_session() -> AsyncSession:
    async with session_manager.manage_session() as session:
        return session

class DefaultBase(DeclarativeBase):
    pass