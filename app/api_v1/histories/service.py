from dataclasses import dataclass

from app.api_v1.histories.schemas import (
    HistorySchema,
    HistorySchemaBase,
    HistoryCreateSchema,
)
from api_v1.histories.repository import HistoryRepository


@dataclass
class HistoryService:
    history_repo: HistoryRepository

    async def create_history(self, new_history: HistoryCreateSchema):
        last_history = await self.history_repo.read_last_history(new_history.user_id)
        city = "" if not last_history else last_history.city
        if city == new_history.city:
            return
        await self.history_repo.create_history(new_history=new_history)

    async def read_user_histories(self, user_id: int) -> list[HistorySchemaBase]:
        histories = await self.history_repo.read_user_histories(user_id=user_id)
        history_schema = [
            HistorySchema.model_validate(history) for history in histories
        ]
        return history_schema

    async def read_last_history(self, user_id: str) -> HistorySchema:
        history = await self.history_repo.read_last_history(user_id=user_id)
        if history is None:
            return None
        response = HistorySchema.model_validate(history)
        return response
