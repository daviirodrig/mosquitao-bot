import discord
import random

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


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
    if message.content.startswith('$pintao'):
        await client.send_file(message.channel, 'pintao.png')
    elif message.content.startswith('$felps'):
        await client.send_file(message.channel, 'felps.png')
    elif message.content.startswith('$ping'):
        await client.send_message(message.channel, 'Pong!')
    elif message.content.startswith('$pergunta'):
        await client.send_message(message.channel, random.choice(["Sim",
                                                                  "Talvez",
                                                                  "Eu sei lá porra",
                                                                  "Não"]))


client.run('NDUyNTM5MjAyNzY5Mzg3NTQw.DfSrBA.qSY-v5iWRuim-xpv2_23T6Xd79M')
