from cmds.helpers.consts import (
    YT_CLIENT_ID,
    YT_CLIENT_SECRET,
    YT_PLAYLIST,
    YT_REFRESH_TOKEN,
)
import time
import aiohttp


class YT:
    access_token = None
    token_expire = None
    playlist_url = f"https://www.youtube.com/playlist?list={YT_PLAYLIST}"

    async def get_token(self):
        if self.access_token and int(time.time()) < self.token_expire:
            # if we already have a access_token and is not expired return it.
            return self.access_token

        req_body = {
            "client_id": YT_CLIENT_ID,
            "client_secret": YT_CLIENT_SECRET,
            "refresh_token": YT_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://oauth2.googleapis.com/token", data=req_body
            ) as r:
                response = await r.json()
                self.access_token = response["access_token"]
                self.token_expire = int(time.time()) + response["expires_in"]
                return response["access_token"]

    async def insert_to_playlist(self, video_id):
        access_token = await self.get_token()
        req_body = {
            "snippet": {
                "playlistId": YT_PLAYLIST,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        }

        headers = {"Authorization": f"Bearer {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
                json=req_body,
                headers=headers,
            ) as r:
                return r.status
