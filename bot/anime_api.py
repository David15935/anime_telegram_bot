import httpx

BASE_URL = "https://api.jikan.moe/v4"


async def search_anime(query: str):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/anime", params={"q": query, "limit": 1})
        r.raise_for_status()
        data = r.json()["data"]
        return data[0] if data else None


async def get_anime_by_id(mal_id: int):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/anime/{mal_id}")
        r.raise_for_status()
        return r.json()["data"]


async def get_top_anime():
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/top/anime")
        r.raise_for_status()
        return r.json()["data"]


async def get_airing_anime():
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/seasons/now")
        r.raise_for_status()
        return r.json()["data"]
