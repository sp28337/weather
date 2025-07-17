import httpx

from app.settings import settings as s


async def get_histories_client(user_id: str):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/histories/user-histories/{user_id}/"
        histories = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        return histories.json()


async def get_last_history_client(user_id: str):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/histories/last-history/{user_id}/"
        last_history = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        return last_history.json()


async def create_history_client(city: str, user_id: str):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/histories/create/"
        await client.post(
            url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "city": city,
                "user_id": user_id,
            },
        )
