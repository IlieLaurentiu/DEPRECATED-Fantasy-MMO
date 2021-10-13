import os
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3

groups = []
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='mmo ', description=None, case_insensitive=True)

# Sqlite3 DB
connection = sqlite3.connect("E:/Programare/theMMORPG_Bot/MMORPG-Bot/DiscordPy_Bot/Database/PlayerList.db")
cursor = connection.cursor()
#cursor.execute("""CREATE TABLE Players (
#                PlayerName text,
#                PlayerID text
#                Whitelisted integer
#                )""")

connection.commit()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    await ctx.send(f'Successfully loaded {extension}')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    await ctx.send(f'Successfully unloaded {extension}')


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        print(f'{filename[:-3]} has loaded!')

client.run(TOKEN)
