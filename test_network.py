
async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
    r = await client.get("https://api.telegram.org")
    print(r.status_code, r.url)
