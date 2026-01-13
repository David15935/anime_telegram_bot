import httpx

BASE_URL = "https://api.jikan.moe/v4"

async def search_anime(query, page=1):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(
            f"{BASE_URL}/anime",
            params={"q": query, "page": page, "limit": 5}
        )
        r.raise_for_status()
        return r.json()["data"]

async def get_anime_by_id(mal_id):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/anime/{mal_id}/full")
        r.raise_for_status()
        return r.json()["data"]

async def top_anime():
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/top/anime")
        r.raise_for_status()
        return r.json()["data"][:5]

async def airing_anime():
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/seasons/now")
        r.raise_for_status()
        return r.json()["data"][:5]
