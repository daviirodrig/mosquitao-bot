import discord

help = embed = discord.Embed(title="", url="https://mosquitao.glitch.me", color=0xc0c0c0)
embed.set_author(name="Comandos do bot", url="https://mosquitao.glitch.me",
                 icon_url="https://goo.gl/Viy31D")
embed.add_field(name="Democracia [opção1] [opção2]", value="```Inicia uma votação```", inline=False)
embed.add_field(name="Resetarvot", value="```Reseta a votação```", inline=False)
embed.add_field(name="Votar [opção]", value="```Vota em uma votação```", inline=False)
embed.add_field(name="Diga [coisas]", value="```Faz o bot dizer coisas```", inline=False)
embed.add_field(name="Paz", value="```Mostra a foto de um dedo do meio```", inline=False)
embed.add_field(name="Entrar", value="```O bot entra em seu canal de voz```", inline=False)
embed.add_field(name="Sair", value="```O bot sai do canal de voz```", inline=False)
embed.add_field(name="Pintao", value="```Mostra o pintão do alan```", inline=False)
embed.add_field(name="Felps", value="```Mostra uma foto do felps```", inline=False)
embed.add_field(name="Ping", value="```Pong!```", inline=False)
embed.add_field(name="Limpar [Quantidade]", value="```Limpa uma certa quantidade de mensagens.```", inline=False)
embed.add_field(name="Pergunta [Sua pergunta] ", value="```O bot responde perguntas objetivas```", inline=False)
embed.set_footer(text="Prefixo: $")