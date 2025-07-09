from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from .schemas import (
    HistoryCreateSchema,
)


async def get_histories(session: AsyncSession, user_id: str) -> list[History]:
    stmt = select(History).order_by(History.timestamp).limit(10)
    result: Result = await session.execute(stmt)
    histories = result.scalars().all()
    return histories


async def get_user_histories(session: AsyncSession, user_id: str) -> list[History]:
    stmt = (
        select(History)
        .where(History.user_id == user_id)
        .order_by(History.timestamp)
        .limit(10)
    )
    result: Result = await session.execute(stmt)
    histories = result.scalars().all()
    return histories


async def get_last_history(session: AsyncSession, user_id: str) -> History | None:
    stmt = select(History).where(History.user_id == user_id).order_by(desc(History.id))
    result: Result = await session.execute(stmt)
    history = result.scalar()
    return history


async def create_history(
    session: AsyncSession,
    new_history: HistoryCreateSchema,
) -> History:
    history = History(**new_history.model_dump())
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return history
