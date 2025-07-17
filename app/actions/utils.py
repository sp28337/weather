import re


def pluralize(word: str) -> str:
    if re.search(r"[^aeiou]y$", word):
        return re.sub(r"y$", "ies", word)
    return word + "s"


async def increase_requested_city_counter(city: str) -> None:
    from app.clients import (
        get_city_by_name_client,
        create_city_client,
        update_city_partial_client,
    )

    city_from_db = await get_city_by_name_client(city=city)
    if city_from_db:
        await update_city_partial_client(city_id=city_from_db["id"])
    else:
        await create_city_client(city=city, requested=1)
