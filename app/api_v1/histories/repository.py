from dataclasses import dataclass

from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import History


@dataclass
class HistoryRepository:
    session: AsyncSession

    async def create_history(
        self,
        new_history: History,
    ) -> int:
        history = History(
            user_id=new_history.user_id,
            city=new_history.city,
        )
        self.session.add(history)
        await self.session.flush()
        history_id = history.id
        await self.session.commit()
        return history_id

    async def read_history(self, history_id: int) -> History | None:
        stmt = select(History).where(History.id == history_id)
        history: History | None = await self.session.scalar(stmt)
        return history

    async def read_last_history(self, user_id: str) -> History | None:
        stmt = (
            select(History)
            .where(History.user_id == user_id)
            .order_by(desc(History.id))
            .limit(1)
        )
        result: Result = await self.session.execute(stmt)
        history = result.scalar_one_or_none()
        return history

    async def read_user_histories(self, user_id: str) -> list[History]:
        stmt = (
            select(History)
            .where(History.user_id == user_id)
            .order_by(desc(History.id))
            .limit(10)
        )
        result: Result = await self.session.execute(stmt)
        histories = result.scalars().all()
        return histories
