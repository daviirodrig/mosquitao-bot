"""Comandos de música"""
import asyncio
import random
from datetime import timedelta

import discord
import wavelink
import yt_dlp as youtube_dl
from discord.ext import commands
from wavelink.ext import spotify

from cmds.helpers.consts import (
    PLAYLIST_ID,
    SPOTIFY_ID,
    SPOTIFY_SECRET,
    YTDL_FORMAT_OPTIONS,
)
from cmds.helpers.spotify import Spotify
from cmds.helpers.yt_api import YT


async def setup(bot: commands.Bot):
    """
    Setup
    """
    print("Iniciando load dos comandos de musica")
    bot.YT_DL = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)
    bot.yt = YT()
    await bot.add_cog(Music(bot))
    print("Load finalizado")


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        # super().__init__()
        self.bot = bot

        bot.loop.create_task(self.setup_lavalink())

    async def setup_lavalink(self) -> None:
        """
        Create lavalink node
        """
        await self.bot.wait_until_ready()

        await asyncio.sleep(5)

        node = wavelink.Node(uri="http://lavalink:2334", password="youshallnotpass")

        await wavelink.NodePool.connect(
            client=self.bot,
            nodes=[node],
            spotify=spotify.SpotifyClient(
                client_id=str(SPOTIFY_ID), client_secret=str(SPOTIFY_SECRET)
            ),
        )

    async def send_info(self, ctx: commands.Context):
        """
        Coroutine to send embed from `embed_factory`
        """
        emb = await self.embed_factory(ctx)

        await ctx.send(embed=emb)

    async def embed_factory(self, ctx: commands.Context) -> discord.Embed:
        """
        Return embed of current song in `ctx`
        """
        while ctx.voice_client.current is None:
            await asyncio.sleep(1)
        track_info = ctx.bot.YT_DL.extract_info(
            ctx.voice_client.current.uri, download=False
        )
        emb = discord.Embed(
            title=track_info["title"],
            url=track_info["webpage_url"],
            colour=discord.Colour.random(),
        )
        emb.set_author(
            name=f"Canal: {track_info['uploader']}",
            url=track_info["uploader_url"],
        )
        emb.set_thumbnail(url=track_info["thumbnail"])
        emb.add_field(
            name="Duração",
            value=timedelta(seconds=track_info["duration"]),
            inline=True,
        )
        emb.add_field(
            name="Pedido por",
            value=ctx.author.name,
            inline=True,
        )
        emb.set_footer(text="Conectado a " + ctx.voice_client.channel.name)
        return emb

    @commands.command()
    async def play(self, ctx: commands.Context, *, track_name: str):
        """
        Play songs | $play [search|link]
        """
        vc: wavelink.Player = (
            ctx.voice_client
            or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        )

        try:
            track = await wavelink.YouTubeTrack.search(track_name, return_first=False)
        except IndexError:
            return await ctx.send("Nothing found")

        if isinstance(track, wavelink.YouTubePlaylist):
            for t in track.tracks:
                await vc.queue.put_wait(t)
        else:
            await vc.queue.put_wait(track[0])

        if vc.is_playing():
            title = track[0].title if isinstance(track, list) else track.name
            await ctx.send(f"Added to queue {title}")
        else:
            ctx.bot.loop.create_task(self.send_info(ctx))
            next_track = await vc.queue.get_wait()
            await vc.play(next_track)

    @commands.command()
    async def spotify(self, ctx: commands.Context, *, track_name: str):
        """
        Play spotify links
        """
        vc: wavelink.Player = (
            ctx.voice_client
            or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        )

        sp = spotify.decode_url(track_name)

        # gambiarra, please ignore
        if sp["id"] == PLAYLIST_ID:
            sp_client = Spotify(SPOTIFY_ID, SPOTIFY_SECRET)
            pl_tracks = await sp_client.get_playlist_tracks(
                f"spotify:playlist:{sp['id']}"
            )
            for t in pl_tracks:
                artists = [i["name"] for i in t["track"]["artists"]]
                artists_str = " ".join(artists)
                query = f'{artists_str} {t["track"]["name"]}'
                track = wavelink.PartialTrack(query=query)
                await vc.queue.put_wait(track)
        # end of gambiarra
        else:
            if sp is None:
                return ctx.send("Not valid")

            try:
                track = await spotify.SpotifyTrack.search(
                    query=sp["id"], type=sp["type"], return_first=False
                )
            except IndexError:
                return await ctx.send("Nothing found")

            if sp["type"] in (
                spotify.SpotifySearchType.playlist,
                spotify.SpotifySearchType.album,
            ):
                for t in track:
                    await vc.queue.put_wait(t)
            else:
                await vc.queue.put_wait(track[0])

        if vc.is_playing():
            await ctx.send("Added to queue")
        else:
            ctx.bot.loop.create_task(self.send_info(ctx))
            next_track = await vc.queue.get_wait()
            await vc.play(next_track)

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: wavelink.Player, track, reason
    ):  # pylint: disable=unused-argument
        """
        Handle on track end
        """
        if not player.queue.is_empty:
            next_track = await player.queue.get_wait()
            await player.play(next_track)

    @commands.command(aliases=["join"])
    async def entrar(self, ctx):
        """
        Comando para entrar no canal de voz.
        """
        canal_de_voz = ctx.author.voice.channel
        await canal_de_voz.connect()

    @commands.command()
    async def shuffle(self, ctx: commands.Context):
        """
        Randomiza a lista de reprodução
        """
        vc: wavelink.Player = ctx.voice_client
        random.shuffle(vc.queue._queue)  # pylint: disable=protected-access
        await ctx.message.add_reaction("🔀")

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: int = None):
        """
        Altera o volume | $volume {1..500}
        """
        vc: wavelink.Player = ctx.voice_client
        if vc is None:
            return
        if vol is None:
            return await ctx.send(f"Volume: {vc.volume}")
        vol /= 100
        await vc.set_volume(vol, seek=True)
        await ctx.message.add_reaction("🔊")

    @commands.command(aliases=["avançar", "av"])
    async def avancar(self, ctx: commands.Context, pos: int):
        """
        Avança x segundos na música
        """
        if ctx.voice_client is None:
            return
        vc: wavelink.Player = ctx.voice_client
        pos = int(pos * 1000 + vc.position)
        await vc.seek(pos)
        await ctx.message.add_reaction("⏩")

    @commands.command(aliases=["pos"])
    async def position(self, ctx: commands.Context, pos: int):
        """
        Coloca a música em x segundos
        """
        vc: wavelink.Player = ctx.voice_client
        pos *= 1000
        await vc.seek(pos)
        await ctx.message.add_reaction("👍")

    @commands.command()
    async def reconnect(self, ctx: commands.Bot):
        """
        Reconnect to audio server
        """
        ctx.bot.loop.create_task(self.setup_lavalink())

    @commands.command(aliases=["leave", "stop"])
    async def sair(self, ctx):
        """
        Comando para sair do canal de voz.
        """
        if ctx.voice_client is None:
            return
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["queue"])
    async def lista(self, ctx):
        """
        Lista de músicas
        """
        if ctx.voice_client is None:
            return
        if len(ctx.voice_client.queue) < 1:
            return await ctx.send("```css\nLista vazia\n```")
        msg = "```css"
        for i, song in enumerate(ctx.voice_client.queue):
            msg += f"\n{i+1} - {song.title}"
            if len(msg) > 1500:
                break
        msg += "\n```"
        await ctx.send(msg)

    @commands.command()
    async def pause(self, ctx):
        """
        Pausa a música
        """
        if ctx.voice_client is None:
            return
        await ctx.voice_client.pause()
        await ctx.message.add_reaction("⏸")

    @commands.command()
    async def resume(self, ctx):
        """
        Resume a música
        """
        if ctx.voice_client is None:
            return
        await ctx.voice_client.resume()
        await ctx.message.add_reaction("▶")

    @commands.command(aliases=["skip"])
    async def pular(self, ctx):
        """
        Pula a música
        """
        vc: wavelink.Player = ctx.voice_client
        await vc.stop()
        if not vc.queue.is_empty:
            await ctx.send(f"Now playing: {vc.queue[0].title or vc.queue}")

    @commands.command(aliases=["tocando", "nowplaying", "tocandoagora"])
    async def np(self, ctx):
        """
        O que está tocando?
        """

        emb = await self.embed_factory(ctx)

        await ctx.send(embed=emb)

    @commands.command()
    async def playlist(self, ctx, *args):
        yt = ctx.bot.yt
        if not args:
            return await ctx.send("Você precisa digitar url ou add após o comando.")
        if args[0] == "url":
            return await ctx.send(yt.playlist_url)
        if args[0] == "add":
            video_id = ctx.bot.YT_DL.extract_info(args[1], download=False)["id"]
            video_id = args[1].split("=")[1]
            insert = await yt.insert_to_playlist(video_id)
            if insert != 200:
                return await ctx.send(
                    "Algum erro ocorreu e a música não foi adicionada."
                )
            else:
                return await ctx.send("Música adicionada.")
