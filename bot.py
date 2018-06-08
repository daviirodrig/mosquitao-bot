import discord
import random

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
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
    if message.author == client.user:
        return
    elif message.content.startswith('$laranjo'):
        await client.send_message(message.channel, 'Comando não criado.')
        print('{}: $laranjo'.format(message.author))
    elif message.content.startswith('$paz'):
        await client.send_file(message.channel, 'paz.jpg')
        print('{}: $paz'.format(message.author))
    elif message.content.startswith('$pintao'):
        await client.send_file(message.channel, 'pintao.png')
        print('{}: $pintao'.format(message.author))
    elif message.content.startswith('$felps'):
        await client.send_file(message.channel, 'felps.png')
        print('{}: $felps'.format(message.author))
    elif message.content.startswith('$ping'):
        await client.send_message(message.channel, 'Pong!')
        print('{}: $ping'.format(message.author))
    elif message.content.startswith('$pergunta'):
        await client.send_message(message.channel, random.choice(["Sim",
                                                                  "Talvez",
                                                                  "Eu sei lá porra",
                                                                  "Não"]))
        print('{}: $pergunta'.format(message.author))


client.run('NDUyNTM5MjAyNzY5Mzg3NTQw.DfSrBA.qSY-v5iWRuim-xpv2_23T6Xd79M')
