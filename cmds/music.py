"""Comandos de música"""
import random
import asyncio
import os
from cmds.helpers.consts import YTDL_FORMAT_OPTIONS
import discord
import youtube_dl
from datetime import timedelta
from discord.ext import commands

# TODO: implement wavelink


def setup(bot):
    """
    Setup
    """
    print("Iniciando load dos comandos de musica")
    bot.YT_DL = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)
    bot.song_queue = []
    bot.ta_playando = None
    bot.add_cog(Music())
    print("Load finalizado")


class Music(commands.Cog):
    @commands.command(aliases=["join"])
    async def entrar(self, ctx):
        """
        Comando para entrar no canal de voz.
        """
        canal_de_voz = ctx.author.voice.channel
        await canal_de_voz.connect()

    @commands.command(aliases=["leave", "stop"])
    async def sair(self, ctx):
        """
        Comando para sair do canal de voz.
        """
        if ctx.voice_client is None:
            return await ctx.send("Nem to conectado em lugar nenhum, ta louco?")
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send(
                    "Você precisa estar conectado em um canal de voz.")
        async with ctx.typing():
            # Limpa o cache da pasta songs
            os.system("rd /s /q songs") if os.name == "nt" else os.system(
                "rm -rf songs")
            song_dl = ctx.bot.YT_DL.extract_info(url)
            if song_dl["_type"] == "playlist":
                for song in song_dl["entries"]:
                    song["ctx"] = ctx
                    song["requester"] = ctx.author
                    song[
                        "song_path"] = f'./songs/{song["extractor"]}-{song["id"]}.{song["ext"]}'
                    song["play_source"] = discord.FFmpegPCMAudio(
                        source=song["song_path"])
                ctx.bot.song_queue.extend(song_dl["entries"])
                if len(song_dl["entries"]) > 1:
                    await ctx.send(
                        f"Adicionei `{len(song_dl['entries'])}` musicas na lista.")
            else:
                song_info = song_dl["entries"][0] if song_dl.get(
                    "entries") else song_dl
                song_info["ctx"] = ctx
                song_info["requester"] = ctx.author
                song_info[
                    "song_path"] = f'./songs/{song_info["extractor"]}-{song_info["id"]}.{song_info["ext"]}'
                ctx.bot.song_queue.append(song_info)
            if ctx.voice_client.is_playing():
                return await ctx.send(
                    f"{ctx.bot.song_queue[-1]['title']} adicionada à lista.")
            emb = discord.Embed(
                title=ctx.bot.song_queue[-1]["title"],
                url=ctx.bot.song_queue[-1]["webpage_url"],
                colour=random.randint(0, 0xFFFFFF),
            )
            emb.set_author(
                name=f"Canal: {ctx.bot.song_queue[0]['uploader']}",
                url=ctx.bot.song_queue[-1]["uploader_url"],
            )
            emb.set_thumbnail(url=ctx.bot.song_queue[-1]["thumbnail"])
            emb.add_field(
                name="Duração",
                value=timedelta(seconds=ctx.bot.song_queue[-1]["duration"]),
                inline=True,
            )
            emb.add_field(name="Pedido por",
                          value=ctx.bot.song_queue[-1]["requester"].name,
                          inline=True)
            emb.set_footer(text="Conectado a " + ctx.voice_client.endpoint)
            ctx.voice_client.play(ctx.bot.song_queue[-1]["play_source"],
                                  after=lambda e: self.play_next(ctx=ctx))
            ctx.bot.ta_playando = ctx.bot.song_queue[-1]
            await ctx.send(embed=emb)

    def play_next(self, ctx):
        if len(ctx.bot.song_queue) <= 1:
            return
        else:
            for i, songa in enumerate(ctx.bot.song_queue):
                if songa["song_path"] == ctx.bot.ta_playando["song_path"]:
                    index = i
                    break
            if ctx.bot.song_queue[index]["ctx"].voice_client.is_playing():
                ctx.bot.song_queue[index]["ctx"].voice_client.stop()
            ctx.bot.song_queue[index + 1]["ctx"].voice_client.play(
                ctx.bot.song_queue[index + 1]["play_source"],
                after=lambda e: self.play_next(ctx=ctx))
            ctx.bot.ta_playando = ctx.bot.song_queue[index + 1]
            emb = discord.Embed(
                title=ctx.bot.song_queue[index + 1]["title"],
                url=ctx.bot.song_queue[index + 1]["webpage_url"],
                colour=random.randint(0, 0xFFFFFF),
            )
            emb.set_author(
                name=f"Canal: {ctx.bot.song_queue[index+1]['uploader']}",
                url=ctx.bot.song_queue[index + 1]["uploader_url"],
            )
            emb.set_thumbnail(url=ctx.bot.song_queue[index + 1]["thumbnail"])
            emb.add_field(
                name="Duração",
                value=timedelta(
                    seconds=ctx.bot.song_queue[index + 1]["duration"]),
                inline=True,
            )
            emb.add_field(
                name="Pedido por",
                value=ctx.bot.song_queue[index + 1]["requester"].name,
                inline=True,
            )
            emb.set_footer(
                text="Conectado a " +
                ctx.bot.song_queue[index + 1]["ctx"].voice_client.endpoint)
            asyncio.run_coroutine_threadsafe(
                ctx.bot.song_queue[index + 1]["ctx"].send(embed=emb), ctx.bot.loop)
            del ctx.bot.song_queue[index]

    @commands.command(aliases=["queue"])
    async def lista(self, ctx):
        """
        Lista de músicas
        """
        if len(ctx.bot.song_queue) < 1:
            return await ctx.send("```css\nLista vazia\n```")
        msg = "```css"
        for i, song in enumerate(ctx.bot.song_queue):
            msg += f"\n{i+1} - {song['title']}"
        msg += "\n```"
        await ctx.send(msg)

    @commands.command()
    async def pause(self, ctx):
        """
        Pausa a música
        """
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """
        Resume a música
        """
        ctx.voice_client.resume()

    @commands.command(aliases=["skip"])
    async def pular(self, ctx):
        """
        Pula a música
        """
        await self.play_next(ctx)

    @commands.command(aliases=["tocando", "nowplaying", "tocandoagora"])
    async def np(self, ctx):
        """
        O que está tocando?
        """
        emb = discord.Embed(
            title=ctx.bot.ta_playando["title"],
            url=ctx.bot.ta_playando["webpage_url"],
            colour=random.randint(0, 0xFFFFFF),
        )
        emb.set_author(
            name=f"Canal: {ctx.bot.ta_playando['uploader']}",
            url=ctx.bot.ta_playando["uploader_url"],
        )
        emb.set_thumbnail(url=ctx.bot.ta_playando["thumbnail"])
        emb.add_field(
            name="Duração",
            value=timedelta(seconds=ctx.bot.ta_playando["duration"]),
            inline=True,
        )
        emb.add_field(name="Pedido por",
                      value=ctx.bot.ta_playando["requester"].name,
                      inline=True)
        emb.set_footer(text="Conectado a " +
                       ctx.bot.ta_playando["ctx"].voice_client.endpoint)
        await ctx.send(embed=emb)
