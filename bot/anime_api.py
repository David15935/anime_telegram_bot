import httpx

BASE_URL = "https://api.jikan.moe/v4"

# -------------------- SEARCH ANIME --------------------
async def search_anime(query: str):
    """
    Search anime by name.
    Returns a list of dicts with 'mal_id' and 'title'.
    """
    url = f"{BASE_URL}/anime"
    params = {"q": query, "limit": 5}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if not data:
            return []
        # Return first result for details
        return data[0]

# -------------------- GET ANIME BY ID --------------------
async def get_anime_by_id(mal_id: int):
    """
    Fetch full anime details by MAL ID
    """
    url = f"{BASE_URL}/anime/{mal_id}/full"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]

# -------------------- TOP ANIME --------------------
async def get_top_anime():
    """
    Fetch top anime
    """
    url = f"{BASE_URL}/top/anime"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params={"limit": 10})
        resp.raise_for_status()
        return resp.json().get("data", [])

# -------------------- AIRING ANIME --------------------
async def get_airing():
    """
    Fetch currently airing anime
    """
    url = f"{BASE_URL}/seasons/now"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json().get("data", [])

# -------------------- WALLPAPERS --------------------
async def get_wallpapers():
    """
    Returns a static list of wallpaper URLs.
    You can expand this to use another API if you want.
    """
    # Example wallpapers (replace with real endpoint if available)
    return [
        "https://wallpaperaccess.com/full/221342.jpg",
        "https://wallpaperaccess.com/full/1080151.jpg",
        "https://wallpaperaccess.com/full/1080155.jpg",
    ]
