""" Main file to run the bot """
import datetime
import traceback
from discord.ext import commands
from cmds.helpers.consts import OWNER_ID, TOKEN

bot = commands.Bot(command_prefix="$", case_insensitive=True)


@bot.event
async def on_ready():
    """
    Função para quando o bot iniciar
    """
    print("----------------------------")
    print(
        f"Bot iniciado {datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-3)))}"
    )
    print(f"Logado como {bot.user.name}")
    print("----------------------------")


@bot.event
async def on_command_error(ctx, error):
    """
    Função para lidar com erros em comandos
    """
    error = getattr(error, "original", error)
    if hasattr(ctx.command, "on_error"):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(
            "Este comando prescisa de algum argumento\n"
            "Manda um `$help` para ver os comandos"
        )
    if isinstance(error, commands.BadArgument):
        return await ctx.send("Erro no argumento")
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("Comando não encontrado :/")
    canal = bot.get_user(OWNER_ID)
    if canal is None:
        canal = await bot.fetch_user(OWNER_ID)
    error = traceback.format_exception(type(error), error, error.__traceback__)
    error_str = "".join(error)
    return await canal.send(
        f"O comando `{ctx.command}` invocado por `{ctx.author.name}`\n"
        f"Gerou o seguinte erro:\n"
        f"```{error_str}```"
    )


@bot.event
async def on_command(ctx):
    """
    Função para printar quando alguém usar comandos.
    """
    print(
        f"{datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-3)))} {ctx.message.author}: {ctx.message.content}"
    )


@bot.event
async def on_member_join(member):
    """
    Função para quando alguém entrar no servidor.
    """
    try:
        if member.id == bot.user.id:
            return
        canal = bot.get_channel(297130716985032714)
        msg = f"{member.mention} Entrou no Clã Do Mosquito, ae caraiou"
        await canal.send(msg)
    except AttributeError:
        pass


@bot.event
async def on_member_remove(member):
    """
    Função para quando alguém sair do servidor.
    """
    try:
        if member.id == bot.user.id:
            return
        canal = bot.get_channel(297130716985032714)
        msg = f"{member.name} Saiu do clã, kkk otário"
        await canal.send(msg)
    except AttributeError:
        pass


bot.load_extension("cmds.img")
bot.load_extension("cmds.misc")
bot.load_extension("cmds.music")
bot.load_extension("cmds.voting")
bot.run(TOKEN)
