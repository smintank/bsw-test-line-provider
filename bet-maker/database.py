from sqlalchemy.orm import declarative_base

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


Base = declarative_base()

if settings.debug:
    async_engine = create_async_engine('sqlite+aiosqlite:///./debug.db', echo=True)
else:
    async_engine = create_async_engine(settings.postgres_url, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

