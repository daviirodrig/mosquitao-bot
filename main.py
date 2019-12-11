""" Main file to run the bot """
import os
import time
import random
import praw
import prawcore
import requests
import youtube_dl
import discord
from discord.ext import commands
from secret import TOKEN, REDDIT_SECRET, REDDIT_ID
from chanGet import main as getChan


bot = commands.Bot(command_prefix='$', case_insensitive=True)
# bot.remove_command('help')


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
        return await ctx.send('Este comando prescisa de algum argumento\n'
                              'Manda um `$help` para ver os comandos')
    if isinstance(error, commands.BadArgument):
        return await ctx.send('Erro no argumento')
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send('Comando não encontrado :/')
    canal = bot.get_user(212680360486633472)
    return await canal.send(f'O comando `{ctx.command}` invocado por `{ctx.author.name}`\n'
                            f'Gerou o erro: `{type(error)}`\n'
                            f'Args: `{error.args}`\n')


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
            return
        else:
            canal = bot.get_channel(297130716985032714)
            msg = f"{member.mention} Saiu do clã, kkk otário"
            await canal.send(msg)
    except AttributeError:
        pass

# Comandos de Música
YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': './songs/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
YT_DL = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)
FFMPEG_OPTIONS = {
    'options': '-vn'
}

class YTDLSource(discord.PCMVolumeTransformer):
    """
    Pegar do yt
    """
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop
        data = await loop.run_in_executor(None, lambda: YT_DL.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else YT_DL.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)



@bot.command()
async def play(ctx, *, url):
    """
    Comando para tocar música
    """
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=False)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Tocando agora: {}'.format(player.title))


@bot.command()
async def stream(ctx, *, url):
    """
    Comando para tocar música
    """
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Tocando agora: {}'.format(player.title))


@stream.before_invoke
@play.before_invoke
async def certeza_que_entrou(ctx):
    """
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    """
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Você precisa estar conectado à um canal de voz.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


@bot.command()
async def entrar(ctx):
    """
    Comando para entrar no canal de voz.
    """
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so')
    canal_de_voz = ctx.author.voice.channel
    await canal_de_voz.connect()


@bot.command()
async def sair(ctx):
    """
    Comando para sair do canal de voz.
    """
    await ctx.voice_client.disconnect()


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
async def jesus(ctx):
    """
    Reinicia o bot
    """
    if ctx.author.id == 212680360486633472:
        await ctx.send('Flws ae seus judeus kkk')
        heroku_api = f'https://api.heroku.com/apps/mosquitao-bot/dynos/worker'
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer a417cff6-36a3-4fdb-b5d5-3ecd3a5177e9', 'Accept': 'application/vnd.heroku+json; version=3'}
        requests.delete(heroku_api, headers=headers)
    else:
        await ctx.send('Você não tem permissão para usar este comando!')


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
    redd = praw.Reddit(client_id=REDDIT_ID,
                       client_secret=REDDIT_SECRET,
                       user_agent='python/requests:mosquitaobot:1.0 (by /u/davioitu)')
    if subreddits is None:
        sub = redd.random_subreddit(nsfw=False)
    elif str(subreddits).lower() == 'nsfw':
        sub = redd.random_subreddit(nsfw=True)
    else:
        try:
            sub = redd.subreddit(subreddits)
            print(sub.subreddit_type)
        except prawcore.exceptions.Forbidden:
            try:
                sub.quaran.opt_in()
                sub = redd.subreddit(subreddits)
            except prawcore.exceptions.Forbidden:
                await ctx.send('O subreddit escolhido não existe ou não é publico.')
                return
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


@bot.command(usage="[algo]")
async def diga(ctx, *, frase):
    """
    Faz o bot dizer algo.
    """
    await ctx.send(frase)


@bot.command(usage="[@alguém]")
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
