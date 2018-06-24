import discord

help = embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me",
                 icon_url="https://goo.gl/Viy31D")
embed.add_field(name="Diga [coisas]", value="```Faz o bot dizer coisas```", inline=True)
embed.add_field(name="Paz", value="```Mostra a foto de um dedo do meio```", inline=True)
embed.add_field(name="Entrar", value="```O bot entra em seu canal de voz```", inline=True)
embed.add_field(name="Sair", value="```O bot sai do canal de voz```", inline=True)
embed.add_field(name="Pintao", value="```Mostra o pintão do alan```", inline=True)
embed.add_field(name="Felps", value="```Mostra uma foto do felps```", inline=True)
embed.add_field(name="Ping", value="```Pong!```", inline=True)
embed.add_field(name="Limpar [Quantidade]", value="```Limpa uma certa quantidade de mensagens.```", inline=True)
embed.add_field(name="Pergunta [Sua pergunta aqui] ", value="```O bot responde perguntas objetivas```",
                inline=True)
embed.set_footer(text="Prefixo: $")
