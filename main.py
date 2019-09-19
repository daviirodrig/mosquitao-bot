""" Main file to run the bot """
import time
import random
import praw
import requests
import discord
from discord.ext import commands
from secret import TOKEN, REDDIT_SECRET, REDDIT_ID
from chanGet import main as getChan


bot = commands.Bot(command_prefix='$', case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_ready():
    """
    Função para quando o bot iniciar
    """
    print('Bot iniciado')
    print(f'Logado como {bot.user.name}')
    print('----------------------------')
    if bot.user.name == 'Mosquitão':
        canal = bot.get_user(212680360486633472)
        await canal.send('Bot iniciou')
    await bot.change_presence(activity=
                              discord.Game(name=f'bosta na cara de {len(bot.users)} pessoas'))


@bot.event
async def on_command_error(ctx, error):
    """
    Função para lidar com erros em comandos
    """
    error = getattr(error, 'original', error)
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send('Este comando prescisa de algum argumento'
                              'Manda um `$help` para ver os comandos')
    if isinstance(error, commands.BadArgument):
        return await ctx.send('Erro no argumento')
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send('Comando não encontrado :/')
    canal = bot.get_user(212680360486633472)
    return await canal.send(f'Erro: {type(error)}\nArgs: {error.args}')


@bot.event
async def on_command(ctx):
    """
    Função para printar quando alguém usar comandos.
    """
    hora = int(str(ctx.message.created_at)[11:13]) - 3
    print(f'{ctx.message.created_at:%d/%m/%Y às} {hora}:{ctx.message.created_at:%M:%S}'
          f' {ctx.message.author}: {ctx.message.content}')


@bot.event
async def on_member_join(member):
    """
    Função para quando alguém entrar no servidor.
    """
    try:
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
            print('sou eu')
        else:
            canal = bot.get_channel(297130716985032714)
            msg = f"{member.mention} Saiu do clã, kkk otário"
            await canal.send(msg)
    except AttributeError:
        pass


@bot.command()
async def errou(ctx):
    raise Exception('Errou KKKKK')


# Comandos
@bot.command(usage='@alguém')
async def gnomed(ctx, pessoa: discord.Member):
    """
    Gnoma pessoas.
    """
    gnome = 'https://j.gifs.com/rRKn4E.gif'
    emb = discord.Embed(colour=random.randint(0, 0xFFFFFF, ))
    nome = pessoa.nick if pessoa.nick else pessoa.name
    autor = ctx.author.nick if ctx.author.nick else ctx.author.name
    emb.set_author(name=f'{nome} foi gnomado por {autor}!!')
    emb.set_image(url=gnome)
    await ctx.send(embed=emb)


@bot.command()
async def cat(ctx):
    """
    Manda uma foto aleatória de um gato.
    """
    main_url = 'http://aws.random.cat/meow'
    gato = requests.get(main_url).json()
    json_cat = gato['file']
    emb = discord.Embed(colour=random.randint(0, 0xFFFFFF))
    emb.set_image(url=json_cat)
    await ctx.send(embed=emb)


@bot.command(usage='[Opção 1] [Opção 2]')
async def democracia(ctx, *coisa: str):
    """
    Comando para criar votações democráticas.
    """
    global votos1, votos2, votou, vote, coisas, user_iniciou_vote
    user_iniciou_vote = ctx.author.id
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
    """
    Comando para votar em votações criadas pelo $democracia.
    """
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
    """
    Comando para mostrar resultados da votação.
    """
    if vote:
        if ctx.author.id == user_iniciou_vote:
            await ctx.send(f'Votação encerrada!')
            await ctx.send(f'{votos1} votos para {coisas[0]}'f'\n{votos2} votos para {coisas[1]}')
        else:
            await ctx.send(f'Apenas quem iniciou a votação pode finalizá-la')
    else:
        await ctx.send('Nenhuma votação está ocorrendo no momento')


@bot.command()
async def limpar(ctx, lim: int):
    """
    Comando para limpar mensagens.
    """
    if lim > 30:
        await ctx.send('O Limite máximo de mensangens é `30`')
    await ctx.channel.purge(limit=(lim + 1))
    msg = await ctx.send(f'{lim + 1} mensagens limpas')
    time.sleep(3)
    await msg.delete()


@bot.command()
async def pergunta(ctx):
    """
    O bot responde perguntas objetivas (sim ou não).
    """
    if 'sentido da vida' in ctx.message.content.lower():
        await ctx.send('**42**')
    else:
        await ctx.send(random.choice(["Sim",
                                      "Com certeza",
                                      "Talvez",
                                      "Não"]))


@bot.command()
async def rng(ctx, inicio: int, ate: int, dados: int):
    """
    Comando para gerar números aleatórios.
    """
    if dados > 5:
        await ctx.send('O número máximo de dados é `5`')
        return
    soma = 0
    for number in range(1, dados + 1):
        sort = random.randint(inicio, ate)
        soma += sort
        await ctx.send(f'O {number}º numero sorteado foi {sort}')
    if dados > 1:
        await ctx.send(f'A soma desses números é {soma}')


@bot.command()
async def escolha(ctx, *escolhas: str):
    """
    Comando para deixar o bot escolher entre várias opções.
    """
    await ctx.send('E a opção escolhida foi')
    time.sleep(0.5)
    await ctx.send(random.choice(escolhas))


@bot.command()
async def reddit(ctx, subreddits=None):
    """
    Pega um post aleatório de um subreddit específico ou aleatório
    """
# TODO: Arrumar subreddits quarentenados, privados e banidos
    redd = praw.Reddit(client_id=REDDIT_ID,
                       client_secret=REDDIT_SECRET,
                       user_agent='python/requests:mosquitaobot:1.0 (by /u/davioitu)')
    if subreddits is None:
        sub = redd.random_subreddit(nsfw=False)
    elif str(subreddits).lower() == 'nsfw':
        sub = redd.random_subreddit(nsfw=True)
    else:
        sub = redd.subreddit(subreddits)
    ranpost = sub.random()
    if ranpost is None:
        ranpost = random.choice(list(sub.hot()))
    while len(ranpost.selftext) >= 1024:
        ranpost = sub.random()
        if ranpost is None:
            ranpost = random.choice(list(sub.hot()))
    emb = discord.Embed(title=ranpost.title, url=ranpost.shortlink)
    if ranpost.is_self:
        emb.add_field(value=ranpost.selftext, name='Texto')
    else:
        if ranpost.url[0:17] == 'https://i.redd.it':
            emb.set_image(url=ranpost.url)
        else:
            emb.add_field(name='Link', value=ranpost.url)
    author_url = '/u/' + ranpost.author.name
    sub_name = '/r/' + ranpost.subreddit.display_name.lower()
    emb.set_author(name=sub_name + ' by ' + author_url)
    await ctx.send(embed=emb)


@bot.command()
async def chan(ctx):
    """
    Manda uma foto aleatória do 4chan.
    """
    emb = discord.Embed()
    emb.set_image(url=getChan(1))
    await ctx.send(embed=emb)


@bot.command()
async def ping(ctx):
    """
    Comando para ver a latência do bot.
    """
    msg = await ctx.send('<a:loading:509160083305791488>')
    bot_ms = str(msg.created_at - ctx.message.created_at)
    await msg.edit(content=f'Pong!, `{bot_ms[8:11]}ms`')


# Comandos de Imagem
@bot.command()
async def zap(ctx):
    """
    Engraçadão pô
    """
    await ctx.send(file=discord.File('images/zap.jpg'))


@bot.command()
async def paz(ctx):
    """
    Dedo do meio = Símbolo de paz
    """
    await ctx.send(file=discord.File('images/paz.jpg'))


@bot.command()
async def felps(ctx):
    """
    Felps.
    """
    await ctx.send(file=discord.File('images/felps.png'))


@bot.command()
async def wtf(ctx):
    """
    Excuse me what the fuck?
    """
    await ctx.send(file=discord.File('images/wtf.jpg'))


@bot.command()
async def paiva(ctx):
    """
    Punheta.
    """
    await ctx.send(file=discord.File('images/paiva.png'))


@bot.command()
async def pintao(ctx):
    """
    Mostra o pintão foda do Alan.
    """
    await ctx.send(file=discord.File('images/pintao.png'))


@bot.command()
async def diga(ctx, *, frase):
    """
    Faz o bot dizer algo.
    """
    await ctx.send(frase)


# Comandos gigantes com embed
@bot.command()
async def help(ctx):
    """
    Isso que você tá lendo
    """
    embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
    embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me", icon_url="https://goo.gl/Viy31D")
    embed.add_field(name="Info [@nome]", value="```Mostra informações sobre a pessoa marcada```", inline=True)
    embed.add_field(name="Gnomed [@nome]", value="```Gnoma alguém```", inline=True)
    embed.add_field(name="Cat", value="```Envia uma foto de um gato aleatório```", inline=True)
    embed.add_field(name="Wtf", value="```Excuse me what the fuck```", inline=True)
    embed.add_field(name="Rng [inicio] [fim] [quantidade]", value="```Gera um ou vários números aleatórios\nEx: `$rng 1 20 1` para um D20```", inline=True)
    embed.add_field(name="Democracia [opção1] [opção2]", value="```Inicia uma votação```", inline=True)
    embed.add_field(name="Escolha [coisas]", value="```Escolhe uma das coisas que você digitou```", inline=True)
    embed.add_field(name="Resultados", value="```Mostra o resultado da votação```", inline=True)
    embed.add_field(name="Votar [opção]", value="```Vota em uma votação```", inline=True)
    embed.add_field(name="Chan", value="```Manda uma imagem aleatória de TODO o 4chan```", inline=True)
    embed.add_field(name="Diga [coisas]", value="```Faz o bot dizer coisas```", inline=True)
    embed.add_field(name="Paz", value="```Mostra a foto de um dedo do meio```", inline=True)
    embed.add_field(name="Entrar", value="```O bot entra em seu canal de voz```", inline=True)
    embed.add_field(name="Sair", value="```O bot sai do canal de voz```", inline=True)
    embed.add_field(name="Pintao", value="```Mostra o pintão do alan```", inline=True)
    embed.add_field(name="Felps", value="```Mostra uma foto do felps```", inline=True)
    embed.add_field(name="Paiva", value="```Define paiva com apenas uma imagem```", inline=True)
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
    """
    Pega informações de um usuário
    """
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
