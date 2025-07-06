import re

from app.clients import (
    get_city_by_name,
    create_city,
    update_city_partial,
)


def pluralize(word: str) -> str:
    if re.search(r"[^aeiou]y$", word):
        return re.sub(r"y$", "ies", word)
    return word + "s"


async def increase_requested(city: str) -> None:
    city_from_db = await get_city_by_name(city=city)
    if city_from_db:
        await update_city_partial(city=city_from_db)
    else:
        await create_city(city=city, requested=1)
