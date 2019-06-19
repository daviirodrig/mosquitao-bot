import discord
import os
import time
import random
import requests
from discord.ext import commands
from secret import TOKEN

description = "Um Bot MUITO FODA"
vote = False
bot = commands.Bot(command_prefix='$', description=description, case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot iniciado')
    print(f'Logado como {bot.user.name}')
    print('----------------------------')
    if bot.user.name == 'Mosquitão':
        canal = bot.get_user(212680360486633472) 
        await canal.send('Bot iniciou')
    await bot.change_presence(activity=discord.Game(name=f'bosta na cara de {len(bot.users)} pessoas'))


@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if hasattr(ctx.command, 'on_error'):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send('Este comando prescisa de algum argumento\nManda um `$help` para ver os comandos')
    elif isinstance(error, commands.BadArgument):
        return await ctx.send('Erro no argumento')
    elif isinstance(error, commands.CommandNotFound):
        return await ctx.send('Comando não encontrado :/')
    else:
        print(f'Um erro ocorreu\n{error}')


@bot.event
async def on_command(ctx):
    hora = int(str(ctx.message.created_at)[11:13]) - 3
    print(f'{ctx.message.created_at:%d/%m/%Y às} {hora}:{ctx.message.created_at:%M:%S}'
          f' {ctx.message.author}: {ctx.message.content}')


@bot.event
async def on_member_join(member):
    try:
        canal = bot.get_channel(297130716985032714)
        msg = f"{member.mention} Entrou no Clã Do Mosquito, ae caraiou"
        await canal.send(msg)
    except AttributeError:
        pass


@bot.event
async def on_member_remove(member):
    try:
        if member.id == bot.user.id:
            print('sou eu')
        else:
            canal = bot.get_channel(297130716985032714)
            msg = f"{member.mention} Saiu do clã, kkk otário"
            await canal.send(msg)
    except AttributeError:
        pass


@bot.command()
async def gnomed(ctx, pessoa: discord.Member):
    gnome = 'https://j.gifs.com/rRKn4E.gif'
    ee = discord.Embed(colour=random.randint(0, 0xFFFFFF, ))
    ee.set_author(name=f'{pessoa.nick} foi gnomado por {ctx.author.nick}!!!')
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


@bot.group()
async def democracia(ctx, *coisa: str):
    global votos1, votos2, votou, vote, coisas, user
    user = ctx.author.id
    coisas = []
    votou = []
    vote = True
    votos1 = 0
    votos2 = 0
    for palavra in coisa:
        coisas.append(palavra)
    if len(coisas) != 2:
        if len(coisas) < 2:
            await ctx.send('Este comando precisa de duas opções')
        elif len(coisas) > 2:
            await ctx.send('Este comando suporta apenas duas opções')
    else:
        await ctx.send(f'Digite `$votar 1` para votar em `{coisas[0]}`'
                       f'\nDigite `$votar 2` para votar em `{coisas[1]}` ')


@bot.command()
async def votar(ctx, numero: int):
    global votos1, votos2
    if vote:
        if ctx.author.name in votou:
            await ctx.send(f'Você já votou, {ctx.message.author.mention}')
        else: 
            if numero == 1:
                votos1 += 1
                votou.append(ctx.author.name)
                await ctx.send(f'+1 voto contado para "{coisas[0]}"')
            elif numero == 2:
                votos2 += 1
                votou.append(ctx.author.name)
                await ctx.send(f'+1 voto contado para "{coisas[1]}"')
            else:
                await ctx.send(f'Número de votação inválido {ctx.message.author.mention}')
    else:
        await ctx.send('Nenhuma votação está ocorrendo no momento')


@bot.command()
async def resultados(ctx):
    if vote:
        if ctx.author.id == user:
            await ctx.send(f'Votação encerrada!')
            await ctx.send(f'{votos1} votos para {coisas[0]}'f'\n{votos2} votos para {coisas[1]}')
        else:
            await ctx.send(f'Apenas quem iniciou a votação pode finalizá-la')
    else:
        await ctx.send('Nenhuma votação está ocorrendo no momento')


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
                                      "Não"]))


@bot.command()
async def rng(ctx, de: int, ate: int, dados: int):
    if dados > 5:
        await ctx.send('O número máximo de números é `5`')
        return
    soma = 0
    for x in range(1, dados + 1):
        sort = random.randint(de, ate)
        soma += sort
        await ctx.send(f'O {x}º numero sorteado foi {sort}')
    if dados > 1:
        await ctx.send(f'A soma desses números é {soma}')


@bot.command()
async def run(ctx, cmd):
    await ctx.send(os.system(cmd))


@bot.command()
async def ping(ctx):
    msg = await ctx.send('<a:loading:509160083305791488>')
    ms = str(msg.created_at - ctx.message.created_at)
    await msg.edit(content=f'Pong!, `{ms[8:11]}ms`')

# Comandos de Imagem
@bot.command()
async def otaku(ctx):
    await ctx.send(file=discord.File('images/otaku.png'))


@bot.command()
async def zap(ctx):
    await ctx.send(file=discord.File('images/zap.jpg'))


@bot.command()
async def paz(ctx):
    await ctx.send(file=discord.File('images/paz.jpg'))


@bot.command()
async def felps(ctx):
    await ctx.send(file=discord.File('images/felps.png'))


@bot.command()
async def wtf(ctx):
    await ctx.send(file=discord.File('images/wtf.jpg'))


@bot.command()
async def pintao(ctx):
    await ctx.send(file=discord.File('images/pintao.png'))


@bot.command()
async def diga(ctx, *, frase):
    await ctx.send(frase)


@bot.command()
async def escolha(ctx, *escolhas: str):
    await ctx.send('E a opção escolhida foi')
    time.sleep(0.5)
    await ctx.send(random.choice(escolhas))




# Comandos gigantes com embed
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
    embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me", icon_url="https://goo.gl/Viy31D")
    embed.add_field(name="Info [@nome]", value="```Mostra informações sobre a pessoa marcada```", inline=True)
    embed.add_field(name="Cat", value="```Envia uma foto de um gato aleatório```", inline=True)
    embed.add_field(name="Wtf", value="```Excuse me what the fuck```", inline=True)
    embed.add_field(name="Rng [inicio] [fim] [quantidade]", value="```difGera um ou vários números aleatórios\nEx: `$rng 1 20 1` para um D20```", inline=True)
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
    embed.add_field(name="Zap", value="```😂 👌```", inline=True)
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
    emb.add_field(name=':busts_in_silhouette:| Nome', value=f'```{user.name}```')
    emb.add_field(name=':pencil:| Apelido', value=f'```{user.nick}```'.replace('None', 'Nenhum'))
    emb.add_field(name=':id:| id', value=f'```{user.id}```')
    emb.add_field(name=':robot:| É Bot?', value=f'```{user.bot}```'.replace('False', 'Não').replace('True', 'Sim'))
    emb.add_field(name=':alarm_clock:| Criado em', value=f'```{user.created_at:%d-%m-%Y às %H:%M:%S}```')
    emb.add_field(name=':large_blue_circle:| Status',
                  value=f'```{user.status}```'.replace('dnd', 'Não pertubar').replace('idle', 'Ausente').replace(
                      'online', 'Disponível'))
    emb.add_field(name=':calendar:| Entrou no clã em', value=f'```{user.joined_at:%d-%m-%Y às %H:%M:%S}```')
    if user.activity is not None:
        if user.activity.name == 'Spotify':
            emb.add_field(name=':loud_sound:| Ouvindo', value=f'```{user.activity.title} - {user.activity.artist}```')
        else:
            emb.add_field(name=':joystick:| Game', value=f'```{user.activity.name}```'.replace('None', 'Nenhum'))
    else:
        emb.add_field(name=':joystick:| Game', value='```Nenhum```')
    emb.set_footer(text=f'Pedido por: {ctx.author.name + ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


bot.run(TOKEN)
