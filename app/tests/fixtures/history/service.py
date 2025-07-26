import pytest_asyncio

from app.api_v1.histories.service import HistoryService


@pytest_asyncio.fixture
def mock_history_service(
    fake_history_repository,
):
    return HistoryService(
        history_repo=fake_history_repository,
    )
