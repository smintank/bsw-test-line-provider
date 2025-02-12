from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

if settings.debug:
    DATABASE_URL = 'sqlite+aiosqlite:///./debug.db'
else:
    DATABASE_URL = (f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
                    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")

Base = declarative_base()

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
