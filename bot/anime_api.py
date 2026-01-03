import requests
import random

JIKAN = "https://api.jikan.moe/v4"

def search_anime(query):
    r = requests.get(f"{JIKAN}/anime", params={"q": query, "limit": 1})
    return r.json()["data"]

def top_anime():
    r = requests.get(f"{JIKAN}/top/anime", params={"limit": 5})
    return r.json()["data"]

def airing_anime():
    r = requests.get(f"{JIKAN}/seasons/now", params={"limit": 5})
    return r.json()["data"]

def anime_wallpaper():
    # Safe anime wallpaper API
    r = requests.get("https://api.waifu.pics/sfw/waifu")
    return r.json()["url"]
