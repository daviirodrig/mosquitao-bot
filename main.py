import discord
import time
import random
import requests
from discord.ext import commands
from secret import TOKEN

description = "Um Bot MUITO FODA"
bot = commands.Bot(command_prefix='$', description=description)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('AE CARAIO')
    print(f'LOGGED COMO {bot.user.name}')
    print('----------------------------')


@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if hasattr(ctx.command, 'on_error'):
        return

    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'gnomed':
            return await ctx.send(f'Não consegui achar este membro.')


@bot.event
async def on_command(ctx):
    print(f'{ctx.message.created_at:%d-%m-%Y às %H:%M:%S} {ctx.message.author}: {ctx.message.content}')


@bot.event
async def on_member_join(ctx, member):
    msg = f"{member.mention} Entrou no Clã Do Mosquito, ae caraiou"
    await ctx.send(msg)


@bot.event
async def on_member_remove(ctx, member):
    canal = bot.get_channel("297130716985032714")
    msg = f"{member.mention} Saiu do clã, kkk otário"
    await ctx.send(canal, msg)


@bot.command()
async def gnomed(ctx, pessoa: discord.Member):
    gnome = 'https://j.gifs.com/rRKn4E.gif'
    ee = discord.Embed(colour=random.randint(0, 0xFFFFFF, ))
    ee.set_author(name=f'{pessoa.name} foi gnomado por {ctx.author.name}!!!!!')
    ee.set_image(url=gnome)
    await ctx.send(embed=ee)


@bot.command()
async def cat(ctx):
    main_url = 'http://aws.random.cat/meow'
    gato = requests.get(main_url).json()
    json_cat = gato['file']
    e = discord.Embed(colour=random.randint(0, 0xFFFFFF))
    e.set_image(url=json_cat)
    await ctx.send(embed=e)


"""
@bot.command()
async def democracia(ctx, *opcoes: str):
    votou = []
    vote = True
    votos1 = 0
    votos2 = 0
    await ctx.send('Calma ae que esse comando n ta pronto ainda')

"""


@bot.command()
async def limpar(ctx, lim: int):
    await ctx.channel.purge(limit=(lim + 1))
    msg = await ctx.send(f'{lim + 1} mensagens limpas')
    time.sleep(3)
    await msg.delete()


@bot.command()
async def pergunta(ctx):
    if 'sentido da vida' in ctx.message.content.lower():
        await ctx.send('**42**')
    else:
        await ctx.send(random.choice(["Sim",
                                      "Com certeza",
                                      "Talvez",
                                      "Eu sei lá porra",
                                      "Não"]))


@bot.command()
async def ping(ctx):
    msg = await ctx.send('<a:loading:509160083305791488>')
    ms = str(msg.created_at - ctx.message.created_at)
    await msg.edit(content=f'Pong!, `{ms[8:11]}ms`')


@bot.command()
async def paz(ctx):
    await ctx.send(file=discord.File('images/paz.jpg'))


@bot.command()
async def felps(ctx):
    await ctx.send(file=discord.File('images/felps.png'))


@bot.command()
async def pintao(ctx):
    await ctx.send(file=discord.File('images/paz.jpg'))


@bot.command()
async def diga(ctx, *coisas):
    frase = ''
    for word in coisas:
        frase += word
        frase += ' '
    await ctx.send(frase)


@bot.command()
async def escolha(ctx, *escolhas: str):
    await ctx.send('E a opção escolhida foi')
    time.sleep(1)
    await ctx.send(random.choice(escolhas))


@bot.command()
async def wtf(ctx):
    await ctx.send(file=discord.File('images/wtf.jpg'))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
    embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me", icon_url="https://goo.gl/Viy31D")
    embed.add_field(name="Info [@nome]", value="```Mostra informações sobre a pessoa marcada```", inline=True)
    embed.add_field(name="Cat", value="```Envia uma foto de um gato aleatório```", inline=True)
    embed.add_field(name="Democracia [opção1] [opção2]", value="```Inicia uma votação```", inline=True)
    embed.add_field(name="Escolha [coisas]", value="```Escolhe uma das coisas que você digitou```", inline=True)
    embed.add_field(name="Resultados", value="```Mostra o resultado da votação```", inline=True)
    embed.add_field(name="Votar [opção]", value="```Vota em uma votação```", inline=True)
    embed.add_field(name="Diga [coisas]", value="```Faz o bot dizer coisas```", inline=True)
    embed.add_field(name="Paz", value="```Mostra a foto de um dedo do meio```", inline=True)
    embed.add_field(name="Entrar", value="```O bot entra em seu canal de voz```", inline=True)
    embed.add_field(name="Sair", value="```O bot sai do canal de voz```", inline=True)
    embed.add_field(name="Pintao", value="```Mostra o pintão do alan```", inline=True)
    embed.add_field(name="Felps", value="```Mostra uma foto do felps```", inline=True)
    embed.add_field(name="Ping", value="```Pong!```", inline=True)
    embed.add_field(name="Limpar [Quantidade]", value="```Limpa uma certa quantidade de mensagens.```", inline=True)
    embed.add_field(name="Pergunta [Sua pergunta]", value="```O bot responde perguntas objetivas```", inline=True)
    embed.add_field(name="Help", value="```Isso ae que vc está lendo```", inline=True)
    embed.set_footer(text="Prefixo: $")
    await ctx.send('Mandei na DM')
    await ctx.author.send(embed=embed)


@bot.command()
async def info(ctx, user: discord.Member):
    emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
    emb.set_author(name=f'Informações de {user.name + user.discriminator}')
    emb.set_thumbnail(url=user.avatar_url)
    emb.add_field(name=':bust_in_silhouette:| Nome', value=f'```{user.name}```')
    emb.add_field(name=':pencil:| Apelido', value=f'```{user.nick}```'.replace('None', 'Nenhum'))
    emb.add_field(name=':id:| id', value=f'```{user.id}```')
    emb.add_field(name=':robot:| É Bot?', value=f'```{user.bot}```'.replace('False', 'Não').replace('True', 'Sim'))
    emb.add_field(name=':alarm_clock:| Criado em', value=f'```{user.created_at:%d-%m-%Y às %H:%M:%S}```')
    emb.add_field(name=':large_blue_circle:| Status',
                  value=f'```{user.status}```'.replace('dnd', 'Não pertubar').replace('idle', 'Ausente').replace(
                      'online', 'Disponível'))
    emb.add_field(name=':calendar:| Entrou no clã em', value=f'```{user.joined_at:%d-%m-%Y às %H:%M:%S}```')
    if user.activity is not None:
        emb.add_field(name=':joystick:| Game', value=f'```{user.activity.name}```'.replace('None', 'Nenhum'))
    else:
        emb.add_field(name=':joystick:| Game', value='```Nenhum```')
    emb.set_footer(text=f'Pedido por: {ctx.author.name + ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

bot.run(TOKEN)
