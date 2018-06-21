import discord
import random

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
        if message.author == client.user:
            return

        elif message.content.lower().startswith('$paz'):
            await client.send_file(message.channel, 'images/paz.jpg')
            print('{} {}: {}'.format(tempo, message.author, message.content))

        elif message.content.startswith('$sair'):
            try:
                canaldevoz = client.voice_client_in(message.server)
                await canaldevoz.disconnect()
                await client.send_message(message.channel, ":dvd: Desconectado do canal com sucesso!")
                print('{} {}: {}'.format(tempo, message.author, message.content))
            except AttributeError:
                await client.send_message(message.channel, ":dvd: O bot não está conectado em nenhum canal de voz!")

        elif message.content.lower().startswith('$entrar'):
            try:
                canal = message.author.voice.voice_channel
                await client.join_voice_channel(canal)
                print('{} {}: {}'.format(tempo, message.author, message.content))
            except discord.errors.InvalidArgument:
                await client.send_message(message.channel, ':dvd: Você prescisa estar em um canal de voz!')

        elif message.content.lower().startswith('$pintao'):
            await client.send_file(message.channel, 'images/pintao.png')
            print('{} {}: {}'.format(tempo, message.author, message.content))

        elif message.content.lower().startswith('$felps'):
            await client.send_file(message.channel, 'images/felps.png')
            print('{} {}: {}'.format(tempo, message.author, message.content))

        elif message.content.lower().startswith('$ping'):
            await client.send_message(message.channel, 'Pong!')
            print('{} {}: {}'.format(tempo, message.author, message.content))

        elif message.content.lower().startswith('$pergunta'):
            await client.send_message(message.channel, random.choice(["Sim",
                                                                      "Com certeza",
                                                                      "Talvez",
                                                                      "Eu acho melhor não",
                                                                      "Eu sei lá porra",
                                                                      "Não"]))
            print('{} {}: {}'.format(tempo, message.author, message.content))

        elif message.content.lower().startswith('$'):
            embed = discord.Embed(title="Comando não encontrado", color=0xff0000)
            embed.set_author(name="Mosquitão:", url="https://www.mosquitao.glitch.me")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/459137918318149635.png?v=1")
            await client.send_message(message.channel, embed=embed)
            print('{} {}: {}'.format(tempo, message.author, message.content))


client.run('NDUyNTM5MjAyNzY5Mzg3NTQw.DfSrBA.qSY-v5iWRuim-xpv2_23T6Xd79M')
