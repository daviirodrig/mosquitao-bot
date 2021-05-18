"""Consts file"""
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
REDDIT_ID = getenv("REDDIT_ID")
REDDIT_SECRET = getenv("REDDIT_SECRET")
OWNER_ID = int(getenv("OWNER_ID"))
TOKEN = getenv("MosquitaoToken")
DETA_KEY = getenv("DETA_KEY")
YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "./songs/%(extractor)s-%(id)s.%(ext)s",
    "restrictfilenames": False,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": False,
    "verbose": False,
    "default_search": "auto",
}
