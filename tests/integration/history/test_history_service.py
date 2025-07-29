from datetime import datetime, UTC

import pytest

from pydantic import ValidationError

from app.api_v1.histories.schemas import (
    HistorySchema,
    HistoryCreateSchema,
    HistorySchemaBase,
)
from app.api_v1.histories.service import HistoryService
from app.core.exceptions import HistoryCreateFailException


pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.mark.parametrize(
    "new_history_data, last_history_data, expected_response",
    [
        (
            {"user_id": "a", "city": "Moscow"},
            {"user_id": "q", "city": "Moscow"},
            None,
        ),
        (
            {"user_id": "a", "city": "Berlin"},
            {"user_id": "a", "city": "Berlin"},
            None,
        ),
        (
            {"user_id": "a", "city": "Berlin"},
            {"user_id": "a", "city": "Moscow"},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"user_id": "aaa", "city": "Moscow"},
            None,
            {"user_id": "aaa", "city": "Moscow"},
        ),
        (
            {"user_id": "b", "city": "Paris"},
            {"user_id": "a", "city": "Berlin"},
            {"user_id": "b", "city": "Paris"},
        ),
        (
            {"user_id": "a", "city": "moscow"},
            {"user_id": "a", "city": "Moscow"},
            {"user_id": "a", "city": "moscow"},
        ),
    ],
)
async def test_create_history__success(
    new_history_data,
    last_history_data,
    expected_response,
    history_service: HistoryService,
):
    last_history = (
        HistoryCreateSchema(**last_history_data) if last_history_data else None
    )
    new_history = HistoryCreateSchema(**new_history_data) if new_history_data else None
    response = (
        HistorySchema(
            **expected_response,
            timestamp=datetime.now(UTC).replace(microsecond=0, tzinfo=None),
        )
        if expected_response
        else None
    )
    created_history = await history_service.create_history(
        new_history=new_history,
        last_history=last_history,
    )
    assert response == created_history


@pytest.mark.parametrize(
    "new_history_data, last_history_data",
    [
        (
            {"city": "Moscow"},
            {"user_id": "q", "city": "Moscow"},
        ),
        (
            {"user_id": "a"},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"user_id": 123, "city": "Vladimir"},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"user_id": "user123", "city": 7},
            {"user_id": "user123", "city": "Berlin"},
        ),
        (
            {"user_id": "user123", "city": 7},
            {"user_id": "user123", "city": 7},
        ),
        (
            {"user_id": "user123", "city": {"city": "Moscow"}},
            {"user_id": "user123", "city": "Monaco"},
        ),
        (
            {"user_id": ["user123"], "city": "Vladimir"},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"user_id": "a", "city": "Berlin"},
            {"city": "Moscow"},
        ),
        (
            {"user_id": "a", "city": "Berlin"},
            {"user_id": "a", "citi": "Berlin"},
        ),
        (
            {"user_id": "a", "city": "Berlin"},
            {"user_it": "a", "city": "Berlin"},
        ),
        (
            {"user_id": "aaa", "city": "Moscow"},
            {"user_id": "aaa"},
        ),
        (
            {"user_id": {"132": "123"}},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"asdsd": 132},
            {"user_id": "a", "city": "Berlin"},
        ),
        (
            {"user_id": "a", "city": "moscow"},
            {"ssdas": "safasf"},
        ),
        (
            None,
            {"user_id": "a", "city": "moscow"},
        ),
        (
            {},
            {"user_id": "a", "city": "Moscow"},
        ),
        (
            {"user_id": "a", "city": "Moscow"},
            {"": ""},
        ),
    ],
)
async def test_create_history__fail(
    new_history_data,
    last_history_data,
    history_service: HistoryService,
):
    with pytest.raises((ValidationError, HistoryCreateFailException)):
        last_history = (
            HistoryCreateSchema(**last_history_data) if last_history_data else None
        )
        new_history = (
            HistoryCreateSchema(**new_history_data) if new_history_data else None
        )
        await history_service.create_history(
            new_history=new_history,
            last_history=last_history,
        )


@pytest.mark.parametrize(
    "new_history_data, user_id",
    [
        (
            [
                {"user_id": "a", "city": "Moscow"},
                {"user_id": "a", "city": "Pattaya"},
            ],
            "user123",
        ),
        (
            [
                {"user_id": "user123", "city": "Moscow"},
                {"user_id": "user123", "city": "Pattaya"},
            ],
            "user123",
        ),
        (
            [
                {"user_id": "aser488", "city": "Moscow"},
                {"user_id": "user123", "city": "Pattaya"},
            ],
            "user123",
        ),
    ],
)
async def test_read_user_histories__success(
    new_history_data,
    user_id,
    history_service: HistoryService,
) -> list[HistorySchemaBase]:

    histories = await history_service.read_user_histories(user_id=user_id)

    assert isinstance(histories, list)
    assert len(histories) == 0

    user_histories = [
        await history_service.create_history(new_history=HistoryCreateSchema(**history))
        for history in new_history_data
    ]
    user_histories = user_histories[::-1]

    histories = await history_service.read_user_histories(user_id=user_id)

    for index, history in enumerate(histories):
        assert history == user_histories[index]
        assert isinstance(history.timestamp, datetime)
        assert isinstance(history.city, str)


@pytest.mark.parametrize(
    "new_history_data, user_id, expected_result",
    [
        (
            [
                {"user_id": "user123", "city": "Moscow"},
                {"user_id": "user123", "city": "Pattaya"},
            ],
            "user123",
            HistorySchema(
                city="Pattaya",
                timestamp=datetime.now(UTC).replace(microsecond=0, tzinfo=None),
            ),
        ),
        (
            [
                {"user_id": "aser488", "city": "Moscow"},
                {"user_id": "user123", "city": "Pattaya"},
            ],
            "aser488",
            HistorySchema(
                city="Moscow",
                timestamp=datetime.now(UTC).replace(microsecond=0, tzinfo=None),
            ),
        ),
        (
            [
                {"user_id": "user488", "city": "Moscow"},
                {"user_id": "user123", "city": "Pattaya"},
                {"user_id": "user123", "city": "Bangkok"},
                {"user_id": "user123", "city": "Phuket"},
                {"user_id": "user123", "city": "Samui"},
            ],
            "user123",
            HistorySchema(
                city="Samui",
                timestamp=datetime.now(UTC).replace(microsecond=0, tzinfo=None),
            ),
        ),
        (
            [
                {"user_id": "user488", "city": "Moscow"},
                {"user_id": "user1", "city": "Pattaya"},
                {"user_id": "user2", "city": "Bangkok"},
                {"user_id": "user3", "city": "Phuket"},
                {"user_id": "user4", "city": "Samui"},
            ],
            "user123",
            None,
        ),
        (
            [],
            "user123",
            None,
        ),
    ],
)
async def test_read_last_history__success(
    new_history_data,
    user_id,
    expected_result,
    history_service: HistoryService,
) -> HistorySchema:
    [
        await history_service.create_history(new_history=HistoryCreateSchema(**history))
        for history in new_history_data
    ]
    history = await history_service.read_last_history(user_id=user_id)
    assert isinstance(history, type(expected_result))
