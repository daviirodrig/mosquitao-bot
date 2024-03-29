"""Consts file"""
from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
SPOTIFY_ID = getenv("SPOTIFY_ID")
SPOTIFY_SECRET = getenv("SPOTIFY_SECRET")
SPOTIFY_REFRESH = getenv("SPOTIFY_REFRESH")
PLAYLIST_ID = getenv("PLAYLIST_ID")

YT_PLAYLIST = getenv("YT_PLAYLIST")
YT_CLIENT_ID = getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = getenv("YT_CLIENT_SECRET")
YT_REFRESH_TOKEN = getenv("YT_REFRESH_TOKEN")

REDDIT_AGENT = getenv("REDDIT_AGENT")
REDDIT_ID = getenv("REDDIT_ID")
REDDIT_SECRET = getenv("REDDIT_SECRET")

OWNER_ID = int(getenv("OWNER_ID"))
TOKEN = getenv("MosquitaoToken")
DETA_KEY = getenv("DETA_KEY")

COMMIT_HASH = getenv("COMMIT_HASH")

YTDL_FORMAT_OPTIONS = {
    "outtmpl": "./songs/%(extractor)s-%(id)s.%(ext)s",
    "restrictfilenames": False,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": False,
    "default_search": "auto",
}

boards = [
    'a', 'c', 'w', 'm', 'cgl', 'cm', 'n', 'jp', 'vp', 'v', 'vg', 'vr', 'co',
    'g', 'tv', 'k', 'o', 'an', 'tg', 'sp', 'asp', 'sci', 'int', 'out', 'toy',
    'biz', 'i', 'po', 'p', 'ck', 'ic', 'wg', 'mu', 'fa', '3', 'gd', 'diy',
    'wsg', 's', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 't', 'hr', 'gif', 'trv',
    'fit', 'x', 'lit', 'adv', 'lgbt', 'mlp', 'b', 'r', 'r9k', 'pol', 'soc',
    's4s'
]
