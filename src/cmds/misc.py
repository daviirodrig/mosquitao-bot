"""Comandos aleatórios"""
import asyncio
import random
import time
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from PIL import Image


async def setup(bot):
    """
    Setup
    """
    print("Iniciando load dos comandos de misc")
    await bot.add_cog(Misc())
    print("Load finalizado")


class Misc(commands.Cog):

    @commands.command()
    async def loop(self, ctx, command, times=5):
        """
        Loop de comandos
        """
        if command == "stop":
            ctx.bot.stop_loop = True
            return

        ctx.bot.stop_loop = False

        count = 0
        msg = await ctx.send(f"Loop iniciado: {count}/{times}")

        for _ in range(times):
            if ctx.bot.stop_loop:
                break

            count += 1

            await ctx.invoke(ctx.bot.get_command(command))
            await msg.edit(content=f"Loop iniciado: {count}/{times}")
            await asyncio.sleep(1)

        await ctx.send("Loop finalizado")

    @commands.command(aliases=["rl"])
    async def hotreload(self, ctx, to_rl):
        """
        Recarregar comandos do bot.
        """
        if to_rl == "all":
            await ctx.bot.reload_extension("cmds.img")
            await ctx.bot.reload_extension("cmds.music")
            await ctx.bot.reload_extension("cmds.misc")
            await ctx.bot.reload_extension("cmds.voting")
            return await ctx.send("Reloaded all")
        await ctx.bot.reload_extension(to_rl)
        await ctx.send(f"Reloaded {to_rl}")

    @commands.command()
    async def sync(self, ctx: commands.Context):
        fmt = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(fmt)}")

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context) -> None:
        """
        Latência do bot.
        """
        api_ms = f"{str(round(ctx.bot.latency * 1000))} ms"
        await ctx.send(api_ms)

    @commands.command()
    async def limpar(self, ctx, lim: int):
        """
        Limpar mensagens.
        """
        if lim > 30:
            return await ctx.send("O Limite máximo de mensagens é `30`")
        await ctx.channel.purge(limit=(lim + 1))
        msg = await ctx.send(f"{lim + 1} mensagens limpas")
        time.sleep(3)
        await msg.delete()

    @commands.command()
    async def pergunta(self, ctx):
        """
        O bot responde perguntas objetivas (sim ou não).
        """
        if "sentido da vida" in ctx.message.content.lower():
            await ctx.send("**42**")
        else:
            await ctx.send(random.choice(["Sim", "Com certeza", "Talvez", "Não"]))

    @commands.command()
    async def rng(self, ctx, inicio: int, fim: int, dados: int):
        """
        Gera números aleatórios.
        """
        if dados > 5:
            await ctx.send("O número máximo de dados é `5`")
            return
        soma = 0
        for number in range(1, dados + 1):
            sort = random.randint(inicio, fim)
            soma += sort
            await ctx.send(f"O {number}º numero sorteado foi {sort}")
        if dados > 1:
            await ctx.send(f"A soma desses números é {soma}")

    @commands.command()
    async def escolha(self, ctx, *escolhas: str):
        """
        Faça o bot escolher entre várias opções.
        """
        await ctx.send("E a opção escolhida foi")
        time.sleep(0.5)
        await ctx.send(random.choice(escolhas))

    @commands.command(usage="[algo]")
    async def diga(self, ctx, *, frase):
        """
        Faça o bot dizer algo.
        """
        await ctx.send(frase)

    @commands.command()
    async def emojo(self, ctx, emoji_name):
        """
        Criação automática de emojis :)
        """
        async with ctx.channel.typing():
            async for message in ctx.message.channel.history(limit=50):
                if message.embeds != []:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(message.embeds[0].image.url) as req:
                            img = Image.open(BytesIO(await req.read()))
                    imagem = BytesIO()
                    img.save(imagem, format="PNG" if img.mode == "RGBA" else "JPEG")
                    img = imagem.getvalue()
                    break
                if message.attachments:
                    last_msg = message
                    img = await last_msg.attachments[0].read()
                    break
            emo = await ctx.message.guild.create_custom_emoji(
                name=emoji_name, image=img
            )
            await ctx.send(f"Emoji criado com sucesso! {str(emo)}")

    @commands.command(usage="[@alguém]")
    async def info(self, ctx, user: discord.Member):
        """
        Pega informações de um usuário
        """
        emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
        emb.set_author(name=f"Informações de {user.name + user.discriminator}")
        emb.set_thumbnail(url=user.avatar.url)
        emb.add_field(name=":busts_in_silhouette:| Nome", value=f"```{user.name}```")
        emb.add_field(
            name=":pencil:| Apelido",
            value=f"```{user.nick}```".replace("None", "Nenhum"),
        )
        emb.add_field(name=":id:| id", value=f"```{user.id}```")
        emb.add_field(
            name=":robot:| É Bot?",
            value=f"```{user.bot}```".replace("False", "Não").replace("True", "Sim"),
        )
        emb.add_field(
            name=":alarm_clock:| Criado em",
            value=f"```{user.created_at:%d-%m-%Y às %H:%M:%S}```",
        )
        emb.add_field(
            name=":blue_circle:| Status",
            value=f"```{str(user.status)}```".replace("dnd", "Não pertubar")
            .replace("idle", "Ausente")
            .replace("online", "Disponível"),
        )
        emb.add_field(
            name=":calendar:| Entrou no clã em",
            value=f"```{user.joined_at:%d-%m-%Y às %H:%M:%S}```",
        )
        if user.activity is not None:
            if user.activity.name == "Spotify":
                emb.add_field(
                    name=":loud_sound:| Ouvindo",
                    value=f"```{user.activity.title} - {user.activity.artist}```",
                )
            else:
                emb.add_field(
                    name=":joystick:| Game",
                    value=f"```{user.activity.name}```".replace("None", "Nenhum"),
                )
        else:
            emb.add_field(name=":joystick:| Game", value="```Nenhum```")
        emb.set_footer(
            text=f"Pedido por: {ctx.author.name + ctx.author.discriminator}",
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=emb)
