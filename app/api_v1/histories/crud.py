from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from .schemas import (
    HistoryCreateSchema,
)


async def create_history(
    session: AsyncSession,
    new_history: HistoryCreateSchema,
) -> History:
    history = History(**new_history.model_dump())
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return history
