from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = (f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
                f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")


async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base = declarative_base()


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
