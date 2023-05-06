import base64
import time
from typing import List

import aiohttp

from cmds.helpers.consts import SPOTIFY_REFRESH


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expire = None
        self.user_token_refresh = SPOTIFY_REFRESH
        self.user_access_token = None
        self.user_access_token_expire = None

    @staticmethod
    def get_id(spotify_input: str):
        # input is uri
        if spotify_input.startswith("spotify:") and len(spotify_input.split(":")) == 3:
            return spotify_input.split(":")[-1]
        # input is url
        else:
            return spotify_input.split("/")[-1].split("?")[0]

    async def get_playlist_json(self, playlist):
        playlist_id = self.get_id(playlist)
        access_token = await self.get_user_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, headers=headers) as res:
                return await res.json()

    async def get_playlist_tracks(self, playlist) -> List:
        pl_json = await self.get_playlist_json(playlist)
        tracks = pl_json["tracks"]["items"]
        next_url = pl_json["tracks"]["next"]
        while next_url:
            access_token = await self.get_user_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(next_url, headers=headers) as res:
                    res = await res.json()
                    next_url = res["next"]
                    tracks.extend(res["items"])
        return tracks

    async def get_user_token(self):
        if self.user_access_token:
            now = int(time.time())
            if now < self.user_access_token_expire:
                return self.user_access_token
        auth_to_encode = f"{self.client_id}:{self.client_secret}".encode("ascii")
        auth_b64 = base64.b64encode(auth_to_encode)
        body = {
            "grant_type": "refresh_token",
            "refresh_token": f"{self.user_token_refresh}",
        }
        header = {"Authorization": f"Basic {auth_b64.decode('ascii')}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://accounts.spotify.com/api/token", data=body, headers=header
            ) as res:
                res_json = await res.json()
                access_token = res_json.get("access_token")
        self.user_access_token = access_token
        self.user_access_token_expire = int(time.time()) + 3600
        return access_token
