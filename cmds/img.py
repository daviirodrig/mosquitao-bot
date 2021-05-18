"""Comandos de imagem"""
import random
import aiohttp
import discord
import asyncpraw
import prawcore
import string
from deta import Deta
from discord.ext import commands
from cmds.helpers.chanGet import main as getChan
from cmds.helpers.consts import REDDIT_ID, REDDIT_SECRET, DETA_KEY

deta = Deta(DETA_KEY)
image_db = deta.Base("images")


def setup(bot):
    """
    Setup
    """
    print("Iniciando load dos comandos de imagem")
    bot.add_cog(Images())
    print("Load finalizado")


class Images(commands.Cog):

    @commands.command(usage="[nome do subreddit]")
    async def reddit(self, ctx, subreddits=None):
        """
        Pega um post aleatório de um subreddit específico ou aleatório
        """
        loop_count = 0
        redd = asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="python/requests:mosquitaobot:1.0 (by /u/davioitu)",
        )
        if subreddits is None:
            sub = await redd.random_subreddit(nsfw=False)
        elif str(subreddits).lower() == "nsfw":
            sub = await redd.random_subreddit(nsfw=True)
        else:
            try:
                sub = await redd.subreddit(subreddits)
                try:
                    await sub.quaran.opt_in()
                except prawcore.exceptions.Forbidden:
                    pass
                a = await sub.random()
                del a
            except (prawcore.exceptions.Forbidden, prawcore.exceptions.NotFound):
                await ctx.send("Aparentemente tem algo errado nesse subreddit :/")
                return
        ranpost = await sub.random()
        if ranpost is None:
            ranpost = random.choice(list(await sub.hot()))
        while ranpost is not None:
            ranpost = (
                await sub.random() if ranpost is not None else random.choice(list(await sub.hot()))
            )
            loop_count += 1
            if ranpost.url.endswith(("jpg", "png", "gif", "jpeg", "bmp")):
                break
            if ranpost.is_self and len(ranpost.selftext) <= 1024:
                emb = discord.Embed(title=ranpost.title, url=ranpost.shortlink)
                emb.add_field(value=ranpost.selftext, name="Texto")
                break
            if loop_count > 10:
                return await ctx.send(
                    "Rodei, rodei esse sub e não achei um post que consiga postar bad bad :/"
                )
        emb = discord.Embed(title=ranpost.title, url=ranpost.shortlink)
        if ranpost.is_self:
            emb.add_field(value=ranpost.selftext, name="Texto")
        elif ranpost.url.endswith(("jpg", "png", "gif")):
            emb.set_image(url=ranpost.url)
        author_name = "/u/" + ranpost.author.name
        sub_name = "/r/" + ranpost.subreddit.display_name
        emb.set_author(name=sub_name + " by " + author_name)
        await redd.close()
        await ctx.send(embed=emb)

    @commands.command()
    async def chan(self, ctx):
        """
        Manda uma foto aleatória do 4chan.
        """
        async with ctx.channel.typing():
            emb = discord.Embed()
            emb.set_image(url=getChan(1))
            await ctx.send(embed=emb)

    @commands.command()
    async def randomps(self, ctx):
        """
        Imagem aleatória do site prntsc
        """
        def gerar_link():
            base_url = "https://prnt.sc/"
            chars = string.ascii_lowercase + string.digits
            for _ in range(0, 6):
                selected_char = random.choice(list(chars))
                base_url += selected_char
            return base_url
        url = gerar_link()
        return await ctx.send(url)

    @commands.command(usage="@alguém")
    async def gnomed(self, ctx, pessoa: discord.Member):
        """
        Gnoma pessoas.
        """
        gnome = "https://j.gifs.com/rRKn4E.gif"
        emb = discord.Embed(
            colour=random.randint(
                0,
                0xFFFFFF,
            )
        )
        nome = pessoa.nick if pessoa.nick else pessoa.name
        autor = ctx.author.nick if ctx.author.nick else ctx.author.name
        emb.set_author(name=f"{nome} foi gnomado por {autor}!!")
        emb.set_image(url=gnome)
        await ctx.send(embed=emb)

    @commands.command()
    async def dog(self, ctx):
        """
        Foto aleatória de doguinho AYAYA
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        foto = None
        async with aiohttp.ClientSession() as session:
            while foto is None or foto.endswith(".mp4"):
                async with session.get("https://random.dog/woof.json") as r:
                    dog_img = await r.json()
                    foto = dog_img["url"]
        emb.set_image(url=foto)
        await ctx.send(embed=emb)

    @commands.command()
    async def cat(self, ctx):
        """
        Foto aleatória de um gato.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                gato = await r.json()
                json_cat = gato["file"]
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url=json_cat)
        await ctx.send(embed=emb)

    # Comandos de img db
    @commands.group(invoke_without_command=True)
    async def img(self, ctx, img_name=None):
        if img_name is None:
            await ctx.send("Você precisa digitar uma imagem ou algum dos subcomandos: add, delete ou list")
        else:
            image_db = deta.Base("images")
            res = image_db.get(img_name)
            if res:
                img_url = res["url"]
                emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
                emb.set_image(url=img_url)
                await ctx.send(embed=emb)
            else:
                await ctx.send("Não encontrei essa imagem")

    @img.command()
    async def add(self, ctx, img_name):
        async with ctx.channel.typing():
            async for message in ctx.message.channel.history(limit=50):
                if message.embeds != []:
                    img_url = message.embeds[0].image.url
                    break
                if message.attachments:
                    img_url = message.attachments[0].url
                    break
            image_db = deta.Base("images")
            res = image_db.put({
                "key": img_name,
                "url": img_url,
                "author": ctx.author.name
            })
            await ctx.send(f"`{img_name}` adicionado às imagens")

    @img.command()
    async def delete(self, ctx, img_name):
        image_db = deta.Base("images")
        res = image_db.delete(img_name)
        await ctx.send(f"{img_name} removido das imagens")

    @img.command()
    async def list(self, ctx):
        image_db = deta.Base("images")
        images_fetch = next(image_db.fetch())
        images_list = [item["key"] for item in images_fetch]
        images_list_str = ", ".join(images_list)
        await ctx.send(f"Lista de imagens: {images_list_str}")

    @commands.command()
    async def zap(self, ctx):
        """
        Engraçadão pô
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/bW8xeTy.jpg")
        await ctx.send(embed=emb)

    @commands.command()
    async def paz(self, ctx):
        """
        Dedo do meio = Símbolo de paz
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/LfnWoxA.jpg")
        await ctx.send(embed=emb)

    @commands.command()
    async def felps(self, ctx):
        """
        Felps.
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/NSoXoLG.png")
        await ctx.send(embed=emb)

    @commands.command()
    async def wtf(self, ctx):
        """
        Excuse me what the fuck?
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/6C0SewT.jpg")
        await ctx.send(embed=emb)

    @commands.command()
    async def paiva(self, ctx):
        """
        Punheta.
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/iY4MaXu.png")
        await ctx.send(embed=emb)

    @commands.command()
    async def pintao(self, ctx):
        """
        Mostra o pintão foda do Alan.
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_image(url="https://i.imgur.com/6MLe4Uw.png")
        await ctx.send(embed=emb)
