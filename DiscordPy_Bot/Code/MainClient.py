import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

groups = []
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix = 'mmo '
no_whitelistCommands = [f'{prefix}start', f'{prefix}help']

client = commands.Bot(command_prefix=prefix, description=None, case_insensitive=True)

# Sqlite3 DB
connection = sqlite3.connect("E:/Programare/theMMORPG_Bot/MMORPG-Bot/DiscordPy_Bot/Database/PlayerList.db")
cursor = connection.cursor()
# cursor.execute("""CREATE TABLE Players (
#                PlayerName text,
#                PlayerID integer
#                )""")
connection.commit()


@client.check_once
async def whitelist(ctx):

    # if the message is in no_whitelistCommands, don't check
    if str(ctx.message.content) in no_whitelistCommands:
        return ctx.message.author.id
    elif str(ctx.message.content) not in no_whitelistCommands:
        try:
            # if the command isn't that, check if the player is whitelisted.
            cursor.execute(f'SELECT * FROM Players WHERE PlayerID == {ctx.message.author.id}')
            isWhitelisted = cursor.fetchone()
            connection.commit()
            return isWhitelisted[1] == ctx.message.author.id
        except TypeError:
            # if the player is not whitelisted send embed error

            whitelistError = discord.Embed(title='Error',
                                               description='You need to type **mmo start** in order to be able to use '
                                                           'other commands.')
            whitelistError.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=whitelistError)



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
