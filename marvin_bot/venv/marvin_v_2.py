import random
import requests
import discord
import asyncio
import youtube_dl
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = ("?", "!", "-")  # any message that starts w  ith any of this prefixes will awake the bot
TOKEN = 'NzI5NzgzODQzNjUyODk0Nzky.XwOArg.XBBXlvrjEoJbbhZOZ6k1jCjXrCs'

client = Bot(command_prefix=BOT_PREFIX)
players = {}


# events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=Game(name="my time"))
    print("logged in as " + client.user.name)


@client.event
async def on_member_join(member):
    await client.send(member.user.name + " hoş gelmişsen ağam, ne getirmişsen!")


@client.event
async def on_member_remove(member):
    await client.send(member.user.name + " gitti arkasından konuşulabilir")


@client.event
async def on_command_error(ctx, error):
    await ctx.send("bra öyle bişe yok ha ")


@client.event
async def on_typing(channel, user, when):
    await channel.send(user.name + " yazıyor, dinleyin")


# custom commands
@client.command(name='magic_ball',
                description='Kinda like a fortune teller and dis type of stuff is prohibited by my believes',
                brief="A ghetto fortune teller",
                aliases=['8ball', "eightball", 'eight_ball'],
                pass_context=True)
async def magic_ball(ctx):
    possible_responses = [
        " As I see it, yes.", "Ask again later.", " Better not tell you now.", " Don’t count on it.", "My reply is no.",
        "Oi cunt go f yourself",
        "Reply hazy, try again.", "Yes.", "You may rely on it."
    ]
    await ctx.send(random.choice(possible_responses) + " , " + ctx.message.author.mention)


@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command()
async def square(ctx, arg):
    squared = int(arg) ** 2
    await ctx.send(arg + " squared is : " + str(squared))


@client.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await ctx.send("moruk 1 bitcoin şu an " + value + " dolar kadar")
    return


@client.command(name='yeet',
                description='write yeet followed by the number of the messages you want to delete',
                brief='message yeeter',
                aliases=['delete', 'banish', 'vanish', 'silaq'],
                pass_context=True)
async def yeet(ctx, amount=10):
    await ctx.channel.purge(limit=(amount + 1))
    await ctx.send(str(amount) + " message(s) yeeted off the cliff")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers: ")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(6)


client.loop.create_task(list_servers())
client.run(TOKEN)
