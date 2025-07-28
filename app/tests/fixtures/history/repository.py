import pytest_asyncio

from dataclasses import dataclass

from app.api_v1.histories.schemas import (
    HistorySchema,
    HistorySchemaTest,
    HistoryCreateSchemaTest,
)


@dataclass
class FakeHistoryRepository:
    def __init__(self):
        self._histories: dict[int, HistorySchemaTest] = {}
        self._current_id: int = 1

    async def create_history(self, new_history: HistoryCreateSchemaTest) -> int:
        histoty_id = self._current_id
        self._histories[histoty_id] = HistorySchemaTest(
            user_id=new_history.user_id,
            timestamp="1994-10-19",
            city=new_history.city,
        )

        self._current_id += 1
        return histoty_id

    async def read_history(self, history_id: int) -> HistorySchema | None:
        return self._histories[history_id]

    async def read_last_history(self, user_id: str) -> HistorySchema | None:
        if len(self._histories.values()) > 0:
            histories_list = sorted(
                self._histories.values(),
                key=lambda h: h.timestamp,
                reverse=True,
            )
            for history in histories_list:
                if history.user_id == user_id:
                    return history
        return None

    async def read_user_histories(self, user_id: str) -> list[HistorySchema]:
        histories = [
            history
            for history in self._histories.values()
            if history.user_id == user_id
        ]
        return histories


@pytest_asyncio.fixture
def fake_history_repository() -> FakeHistoryRepository:
    return FakeHistoryRepository()
