import pytest

from pydantic import ValidationError

from app.api_v1.histories.schemas import (
    HistoryCreateSchemaTest,
    HistorySchemaTest,
    HistorySchemaBase,
    HistorySchema,
)
from app.api_v1.histories.service import HistoryService

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "new_history, last_history, expected_response",
    [
        (
            HistoryCreateSchemaTest(user_id="a", city="Moscow"),
            HistoryCreateSchemaTest(user_id="q", city="Moscow"),
            None,
        ),
        (
            HistoryCreateSchemaTest(user_id="a", city="Berlin"),
            HistoryCreateSchemaTest(user_id="a", city="Berlin"),
            None,
        ),
        (
            HistoryCreateSchemaTest(user_id="a", city="Berlin"),
            HistoryCreateSchemaTest(user_id="a", city="Moscow"),
            HistorySchemaTest(user_id="a", city="Berlin", timestamp="1994-10-19"),
        ),
        (
            HistoryCreateSchemaTest(user_id="aaa", city="Moscow"),
            None,
            HistorySchemaTest(user_id="aaa", city="Moscow", timestamp="1994-10-19"),
        ),
        (
            HistoryCreateSchemaTest(user_id="b", city="Paris"),
            HistoryCreateSchemaTest(user_id="a", city="Berlin"),
            HistorySchemaTest(user_id="b", city="Paris", timestamp="1994-10-19"),
        ),
        (
            HistoryCreateSchemaTest(user_id="a", city="moscow"),
            HistoryCreateSchemaTest(user_id="a", city="Moscow"),
            HistorySchemaTest(user_id="a", city="moscow", timestamp="1994-10-19"),
        ),
    ],
)
async def test_create_history__success(
    new_history, last_history, expected_response, mock_history_service: HistoryService
):
    created_history = await mock_history_service.create_history(
        new_history=new_history, last_history=last_history
    )
    assert expected_response == created_history


@pytest.mark.parametrize(
    "new_history_data, last_history_data, expected_response",
    [
        (
            {"user_id": 123, "city": "Moscow"},
            {"user_id": "123", "city": "Moscow"},
            None,
        ),
        (
            {"user_id": "123", "city": "Moscow" * 11},
            {"user_id": "123", "city": "Moscow"},
            None,
        ),
        ({"user_id": "a", "city": 456}, {"user_id": "a", "city": "Moscow"}, None),
        (
            {"user_id": "   ", "city": "Pattaya"},
            {"user_id": "a", "city": "Pattaya"},
            None,
        ),
        ({"user_id": "a", "city": "   "}, {"user_id": "a", "city": "   "}, None),
        ({"user_id": None, "city": "Berlin"}, None, None),
        ({"city": "Berlin"}, None, None),
        ({"user_id": "aaa"}, None, None),
        (None, None, None),
        ({"user_id": "a"}, None, None),
    ],
)
async def test_create_history__fail(
    new_history_data,
    last_history_data,
    expected_response,
    mock_history_service: HistoryService,
):
    try:
        new_history = (
            HistoryCreateSchemaTest(**new_history_data) if new_history_data else None
        )
    except ValidationError as e:
        print(f"Validation error for new_history_data={new_history_data}: {e}")
        new_history = None

    try:
        last_history = (
            HistoryCreateSchemaTest(**last_history_data) if last_history_data else None
        )
    except ValidationError as e:
        print(f"Validation error for last_history_data={last_history_data}: {e}")
        last_history = None

    try:
        created_history = await mock_history_service.create_history(
            new_history=new_history, last_history=last_history
        )
    except Exception as e:
        print(f"Caught exception in create_history: {e}")
        created_history = None

    assert expected_response == created_history


@pytest.mark.parametrize(
    "valid_user_id, histories_data, expected_result",
    [
        (
            "c",
            {
                0: {"user_id": "a", "city": "Moscow"},
                1: {"user_id": "b", "city": "Vladimir"},
                2: {"user_id": "c", "city": "Kazan"},
                3: {"user_id": "c", "city": "Pattaya"},
            },
            {"length": 2, "city_1": "Kazan", "city_2": "Pattaya"},
        ),
        (
            "e",
            {
                0: {"user_id": "a", "city": "Moscow"},
                1: {"user_id": "b", "city": "Vladimir"},
                2: {"user_id": "c", "city": "Kazan"},
                3: {"user_id": "c", "city": "Pattaya"},
            },
            {"length": 0},
        ),
        (
            "a",
            {
                0: {"user_id": "c", "city": "Vyazniki"},
                1: {"user_id": "b", "city": "Vladimir"},
            },
            {"length": 0},
        ),
    ],
)
async def test_read_user_histories__success(
    valid_user_id: str,
    histories_data,
    expected_result,
    mock_history_service: HistoryService,
) -> list[HistorySchemaBase]:
    for i in range(len(histories_data.values())):
        await mock_history_service.create_history(
            new_history=HistoryCreateSchemaTest(**(histories_data[i]))
        )
    response = await mock_history_service.read_user_histories(user_id=valid_user_id)
    histories = [HistorySchema.model_validate(history) for history in response]

    assert isinstance(histories, list)
    assert len(histories) == expected_result["length"]
    for i in range(len(histories)):
        assert histories[i].city == expected_result[f"city_{i + 1}"]


@pytest.mark.parametrize(
    "invalid_user_id",
    [
        1,
        -1,
        "10",
        ["10", 1, 2],
        1.1,
        None,
        "",
        "    ",
        {1: 1},
        (1, 2),
        -0.123,
    ],
)
async def test_read_user_histories__fail(
    invalid_user_id,
    mock_history_service: HistoryService,
):
    res = await mock_history_service.read_user_histories(user_id=invalid_user_id)
    assert isinstance(res, list)
    assert len(res) == 0


@pytest.mark.parametrize(
    "new_history_data",
    [
        {"user_id": "a", "city": "Moscow"},
        {"user_id": "q", "city": "Pattaya"},
    ],
)
async def test_read_last_history__success(
    new_history_data,
    mock_history_service: HistoryService,
) -> HistorySchema:
    history_create_schema = HistoryCreateSchemaTest(**new_history_data)

    created_history = await mock_history_service.create_history(
        new_history=history_create_schema
    )
    history = await mock_history_service.read_last_history(
        user_id=history_create_schema.user_id
    )

    assert history == created_history
    assert history.city == created_history.city
    assert isinstance(history.city, str)
    assert isinstance(created_history.city, str)


@pytest.mark.parametrize(
    "invalid_user_id",
    [
        1,
        -1,
        "10",
        ["10", 1, 2],
        1.1,
        None,
        "",
        "    ",
        {1: 1},
        (1, 2),
        -0.123,
    ],
)
async def test_read_last_history__fail(
    invalid_user_id,
    mock_history_service: HistoryService,
):
    res = await mock_history_service.read_last_history(user_id=invalid_user_id)
    assert res is None
