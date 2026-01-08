import httpx

BASE_URL = "https://api.jikan.moe/v4"


async def search_anime(query: str):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/anime", params={"q": query, "limit": 1})
        r.raise_for_status()
        data = r.json()
        return data["data"][0] if data["data"] else None


async def get_anime_by_id(mal_id: int):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/anime/{mal_id}/full")
        r.raise_for_status()
        return r.json()["data"]
