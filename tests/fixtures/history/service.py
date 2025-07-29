import pytest_asyncio

from app.api_v1.histories.service import HistoryService
from app.api_v1.histories.repository import HistoryRepository


@pytest_asyncio.fixture
def mock_history_service(
    fake_history_repository,
):
    return HistoryService(
        history_repo=fake_history_repository,
    )


@pytest_asyncio.fixture
def history_service(
    get_db_session,
):
    return HistoryService(
        history_repo=HistoryRepository(session=get_db_session),
    )
