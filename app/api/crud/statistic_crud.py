from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models_db.user_value import UserValue
from app.models_db.users import User
from app.models_db.statistic_users import StatisticUserMapped
from app.models.model import ResponseAPI

async def get_user_values_with_name(db: AsyncSession, email_user: str):
    """Recupera i valori e il nome dell'utente tramite join."""
    stmt = (
        select(UserValue, User.name)
        .join(User, User.token == UserValue.token_user)
        .where(UserValue.user_name == email_user)
    )
    res = await db.execute(stmt)
    return res.all()

async def get_last_user_statistic(db: AsyncSession, email_user: str) -> StatisticUserMapped | None:
    """Recupera l'ultimo snapshot statistico salvato per l'utente."""
    stmt = (
        select(StatisticUserMapped)
        .where(StatisticUserMapped.email == email_user)
        .order_by(StatisticUserMapped.id.desc())
        .limit(1)
    )
    res = await db.execute(stmt)
    return res.scalars().first()

async def get_all_statistic_user(db: AsyncSession, email_user: str) -> StatisticUserMapped | None:
    """Recupera i dati salvati nelle statistiche."""
    try:
        if email_user is None:
            return None
        stmt = (
            select(StatisticUserMapped)
            .where(StatisticUserMapped.email == email_user)
            .order_by(StatisticUserMapped.creations_date.asc())
        )
        res = await db.execute(stmt)
        record = res.scalars().all()
        return record
    except Exception as e:
        return None

async def create_user_statistic(db: AsyncSession, db_statistic: StatisticUserMapped) -> StatisticUserMapped:
    """Salva un nuovo snapshot a database."""
    db.add(db_statistic)
    await db.commit()
    await db.refresh(db_statistic)
    return db_statistic