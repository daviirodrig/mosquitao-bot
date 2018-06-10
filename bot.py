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
    time = message.timestamp
    if message.author == client.user:
        return
    elif message.content.startswith('$laranjo'):
        await client.send_message(message.channel, 'Comando não criado.')
        print('\033[m{} \033[0;31m{}: \033[0;35m$laranjo'.format(time, message.author))
    elif message.content.startswith('$paz'):
        await client.send_file(message.channel, 'paz.jpg')
        print('\033[m{} \033[0;31m{}: \033[0;35m$paz'.format(time, message.author))
    elif message.content.startswith('$pintao'):
        await client.send_file(message.channel, 'pintao.png')
        print('\033[m{} \033[0;31m{}: \033[0;35m$pintao'.format(time, message.author))
    elif message.content.startswith('$felps'):
        await client.send_file(message.channel, 'felps.png')
        print('\033[m{} \033[0;31m{}: \033[0;35m$felps'.format(time, message.author))
    elif message.content.startswith('$ping'):
        await client.send_message(message.channel, 'Pong!')
        print('\033[m{} \033[0;31m{}: \033[0;35m$ping'.format(time, message.author))
    elif message.content.startswith('$pergunta'):
        await client.send_message(message.channel, random.choice(["Sim",
                                                                  "Com certeza",
                                                                  "Talvez",
                                                                  "Eu acho melhor não",
                                                                  "Eu sei lá porra",
                                                                  "Não"]))
        print('{} \033[0;31m{}: \033[0;35m$pergunta'.format(time, message.author))
    elif message.content.startswith('$'):
        await client.send_message(message.channel, 'ESTE COMANDO NÂO EXISTE!!!')


client.run('NDUyNTM5MjAyNzY5Mzg3NTQw.DfSrBA.qSY-v5iWRuim-xpv2_23T6Xd79M')
