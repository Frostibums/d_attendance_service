from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.config.db import db_settings

engine = create_async_engine(db_settings.db_url, echo=False, pool_pre_ping=True)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
print(db_settings.db_url)
Base = declarative_base()


async def get_session():
    async with async_session() as session:
        yield session
