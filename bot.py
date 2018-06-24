import discord
import random
import time

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='Merda na sua cara'))
    print('-' * len(client.user.id))


@client.event
async def on_member_join(member):
    canal = client.get_channel("297130716985032714")
    msg = "{} Entrou no Clã Do Mosquito, ae caraiou".format(member.mention)
    await client.send_message(canal, msg)


@client.event
async def on_member_remove(member):
    canal = client.get_channel("297130716985032714")
    msg = "{} Saiu do clã, kkk otário".format(member.mention)
    await client.send_message(canal, msg)


@client.event
async def on_message(message):
    tempo = message.timestamp
    try:
        if message.author == client.user:
            return

        elif message.content.lower().startswith('$spam'):
            for c in range(0, 15):
                time.sleep(0.7)
                await client.send_message(message.channel, 'Spawna pokemon ae men')

        elif message.content.lower().startswith('$pokedex'):
            await client.send_message(message.channel, 'Comando não implementado')
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$diga'):
            await client.send_message(message.channel, message.content[6:])
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$paz'):
            await client.send_file(message.channel, 'images/paz.jpg')
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$entrar'):
            print(f'{tempo} {message.author}: {message.content}')
            try:
                canal = message.author.voice.voice_channel
                await client.join_voice_channel(canal)
            except discord.errors.InvalidArgument:
                await client.send_message(message.channel, ':dvd: Você prescisa estar em um canal de voz!')

        elif message.content.startswith('$sair'):
            print(f'{tempo} {message.author}: {message.content}')
            try:
                canaldevoz = client.voice_client_in(message.server)
                await canaldevoz.disconnect()
                await client.send_message(message.channel, ":dvd: Desconectado do canal com sucesso!")
            except AttributeError:
                await client.send_message(message.channel, ":dvd: O bot não está conectado em nenhum canal de voz!")

        elif message.content.lower().startswith('$pintao'):
            await client.send_file(message.channel, 'images/pintao.png')
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$felps'):
            await client.send_file(message.channel, 'images/felps.png')
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$ping'):
            await client.send_message(message.channel, 'Pong!')
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$pergunta'):
            if 'sentido da vida' in message.content.lower():
                await client.send_message(message.channel, '**42**')
            await client.send_message(message.channel, random.choice(["Sim",
                                                                      "Com certeza",
                                                                      "Talvez",
                                                                      "Eu acho melhor não",
                                                                      "Eu sei lá porra",
                                                                      "Não"]))
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$help'):
            embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
            embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me",
                             icon_url="https://goo.gl/Viy31D")
            embed.add_field(name="Diga [coisas]", value="```Faz o bot dizer coisas```", inline=True)
            embed.add_field(name="Paz", value="```Mostra a foto de um dedo do meio```", inline=True)
            embed.add_field(name="Entrar", value="```O bot entra em seu canal de voz```", inline=True)
            embed.add_field(name="Sair", value="```O bot sai do canal de voz```", inline=True)
            embed.add_field(name="Pintao", value="```Mostra o pintão do alan```", inline=True)
            embed.add_field(name="Felps", value="```Mostra uma foto do felps```", inline=True)
            embed.add_field(name="Ping", value="```Pong!```", inline=True)
            embed.add_field(name="Pergunta [Sua pergunta aqui] ", value="```O bot responde perguntas objetivas```",
                            inline=True)
            embed.set_footer(text="Prefixo: $")
            await client.send_message(message.channel, embed=embed)
            print(f'{tempo} {message.author}: {message.content}')

        elif message.content.lower().startswith('$'):
            embed = discord.Embed(title="Comando não encontrado",
                                  description="Use $help para ver os comandos disponíveis", color=0xff0000)
            embed.set_author(name="IH DEU RUIM", url="https://mosquitao.glitch.me")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/459137918318149635.png?v=1")
            await client.send_message(message.channel, embed=embed)
            print(f'{tempo} {message.author}: {message.content}')

    except Exception as error:
        dogeminer = '<@!212680360486633472>'
        await client.send_message(message.channel, f'Ei {dogeminer}, deu erro')
        await client.send_message(message.channel, f'Error: [{error}]')
        print(f'{tempo} {message.author}: {message.content}')


client.run('NDUyNTM5MjAyNzY5Mzg3NTQw.DfSrBA.qSY-v5iWRuim-xpv2_23T6Xd79M')
