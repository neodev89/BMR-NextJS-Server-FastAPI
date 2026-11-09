# tests/conftest.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport

from app.main import app  # La tua applicazione FastAPI principale
from app.core.database import Base, get_db

# 1. URL per SQLite in-memory asincrono
DATABASE_URL = "postgresql+psycopg://postgres.nievkcazlxioutxagdpc:d1PZEouwCD6xnikg@aws-1-eu-west-2.pooler.supabase.com:5432/postgres"

# 2. Engine di test con StaticPool (indispensabile per SQLite in-memory)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    poolclass=StaticPool,
)

# 3. Sessionmaker per i test
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Crea le tabelle prima di ogni test e le distrugge alla fine."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    """
        Crea una connessione e una transazione isolata per il test.
        Alla fine del test fa il rollback, così il database dell'app non viene sporcato o alterato.
    """
    connection = await engine.connect()
    transaction = await connection.begin()
    
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()
    

@pytest_asyncio.fixture
async def client(db_session):
    """
    Crea il client HTTP di test sovrascrivendo la dipendenza get_db.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()