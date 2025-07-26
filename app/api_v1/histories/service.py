from dataclasses import dataclass

from app.api_v1.histories.schemas import (
    HistorySchema,
    HistorySchemaBase,
    HistoryCreateSchema,
)
from app.api_v1.histories.repository import HistoryRepository


@dataclass
class HistoryService:
    history_repo: HistoryRepository

    async def create_history(
        self,
        new_history: HistoryCreateSchema,
        last_history: HistorySchema | None = None,  # for tests
    ) -> HistorySchema | None:
        if isinstance(new_history.user_id, str) and last_history is None:
            last_history: HistorySchema | None = (
                await self.history_repo.read_last_history(user_id=new_history.user_id)
            )
        if last_history and last_history.city == new_history.city:
            return None

        history_id = await self.history_repo.create_history(new_history=new_history)
        history = await self.history_repo.read_history(history_id=history_id)
        return HistorySchema.model_validate(history)

    async def read_user_histories(self, user_id: str) -> list[HistorySchemaBase]:
        response = await self.history_repo.read_user_histories(user_id=user_id)
        histories = [HistorySchema.model_validate(history) for history in response]
        return histories

    async def read_last_history(self, user_id: str) -> HistorySchema:
        history = await self.history_repo.read_last_history(user_id=user_id)
        if history is None:
            return None
        response = HistorySchema.model_validate(history)
        return response
