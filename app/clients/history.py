import httpx


async def create_history(city: str, user_id: str):
    async with httpx.AsyncClient() as client:
        url = "http://localhost:8000/api/v1/histories/"
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
