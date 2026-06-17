import pytest
import pytest_asyncio

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from sqlalchemy.pool import NullPool

from app.settings import Settings
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()


_settings = Settings()
db_host = "127.0.0.1" if _settings.DB_HOST == "db" else _settings.DB_HOST
url = f"{_settings.DB_DRIVER}://{_settings.DB_USER}:{_settings.DB_PASSWORD}@{db_host}:{_settings.DB_PORT}/{_settings.DB_NAME}-test"
engine = create_async_engine(url=url, future=True, echo=True, poolclass=NullPool)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
