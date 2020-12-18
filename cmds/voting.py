"""Comandos de votação"""
from discord.ext import commands


def setup(bot):
    """
    Setup
    """
    print("Iniciando load dos comandos de voting")
    bot.user_iniciou_vote = None
    bot.coisas = []
    bot.votou = []
    bot.vote = False
    bot.votos1 = 0
    bot.votos2 = 0
    bot.add_cog(Voting())
    print("Load finalizado")


class Voting(commands.Cog):
    @commands.command()
    async def democracia(self, ctx, *coisa: str):
        """
        Comando para criar votações democráticas.
        """
        ctx.bot.user_iniciou_vote = ctx.author.id
        ctx.bot.coisas = []
        ctx.bot.votou = []
        ctx.bot.vote = True
        ctx.bot.votos1 = 0
        ctx.bot.votos2 = 0
        for palavra in coisa:
            ctx.bot.coisas.append(palavra)
        if len(ctx.bot.coisas) != 2:
            if len(ctx.bot.coisas) < 2:
                await ctx.send("Este comando precisa de duas opções")
            elif len(ctx.bot.coisas) > 2:
                await ctx.send("Este comando suporta apenas duas opções")
        else:
            await ctx.send(
                f"Digite `$votar 1` para votar em `{ctx.bot.coisas[0]}`"
                f"\nDigite `$votar 2` para votar em `{ctx.bot.coisas[1]}` "
            )

    @commands.command()
    async def votar(self, ctx, numero: int):
        """
        Comando para votar em votações criadas pelo $democracia.
        """
        if ctx.bot.vote:
            if ctx.author.name in ctx.bot.votou:
                await ctx.send(f"Você já votou, {ctx.message.author.mention}")
            else:
                if numero == 1:
                    ctx.bot.votos1 += 1
                    ctx.bot.votou.append(ctx.author.name)
                    await ctx.send(f'+1 voto contado para "{ctx.bot.coisas[0]}"')
                elif numero == 2:
                    ctx.bot.votos2 += 1
                    ctx.bot.votou.append(ctx.author.name)
                    await ctx.send(f'+1 voto contado para "{ctx.bot.coisas[1]}"')
                else:
                    await ctx.send(
                        f"Número de votação inválido {ctx.message.author.mention}"
                    )
        else:
            await ctx.send("Nenhuma votação está ocorrendo no momento")

    @commands.command()
    async def resultados(self, ctx):
        """
        Comando para mostrar resultados da votação.
        """
        if ctx.bot.vote:
            if ctx.author.id == ctx.bot.user_iniciou_vote:
                await ctx.send("Votação encerrada!")
                await ctx.send(
                    f"{ctx.bot.votos1} votos para {ctx.bot.coisas[0]}"
                    f"\n{ctx.bot.votos2} votos para {ctx.bot.coisas[1]}"
                )
            else:
                await ctx.send("Apenas quem iniciou a votação pode finalizá-la")
        else:
            await ctx.send("Nenhuma votação está ocorrendo no momento")
