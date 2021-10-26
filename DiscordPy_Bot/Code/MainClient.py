import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import Button, Select, SelectOption, ComponentsBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix = 'mmo '
no_whitelistCommands = [f'{prefix}start']

client = commands.Bot(command_prefix=prefix, description=None, case_insensitive=True)

client.guildCount = 0
# Sqlite3 DB

connection = sqlite3.connect("E:/Programare/theMMORPG_Bot/MMORPG-Bot/DiscordPy_Bot/Database/PlayerList.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Players (
                 PlayerName text NOT NULL,
                 PlayerID integer NOT NULL,
                 CurrentCharacter text NOT NULL,
                 MaxCharacters int DEFAULT 1,
                 CharacterSlots int DEFAULT 1,
                 Level integer DEFAULT 1,
                 Experience real DEFAULT 0,
                 Gold integer DEFAULT 100,
                 Vitality integer DEFAULT 250,
                 MaxVit integer DEFAULT 250,
                 ManaPoints integer DEFAULT 300,
                 MaxMana integer DEFAULT 300,
                 Defense integer DEFAULT 0,
                 Attack integer DEFAULT 0,
                 Intelligence integer DEFAULT 5,
                 SkillPoints integer DEFAULT 0,
                 Evasion integer DEFAULT 0
                 )""")



@client.check_once
async def whitelist(ctx):
    # if the message is in no_whitelistCommands, don't check
    if str(ctx.message.content) in no_whitelistCommands:
        return ctx.message.author.id
    elif str(ctx.message.content) not in no_whitelistCommands:
        try:
            # if the command isn't in not in no_whitelistCommands, check if the player is whitelisted.
            # whitelist needs to return an id otherwise the check will fail
            cursor.execute(f'SELECT * FROM Players WHERE PlayerID = {ctx.message.author.id}')
            isWhitelisted = cursor.fetchone()
            return isWhitelisted[1] == ctx.message.author.id
        except TypeError:
            # if the player is not whitelisted send embed error

            whitelistError = discord.Embed(title='Error',
                                           description='You need to type **mmo start** in order to be able to use '
                                                       'other commands.', color=0x00ff00)
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


# Load and reload cogs
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    loadEmbed = discord.Embed(name='Load', description=f'Cog {extension} has successfully been loaded', color=0x00ff00)
    loadEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=loadEmbed)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    unloadEmbed = discord.Embed(name='Unload', description=f'Cog {extension} has successfully been unloaded',
                                color=0x00ff00)
    unloadEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=unloadEmbed)


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'Cogs.{extension}')
    reloadEmbed = discord.Embed(name='Reload', description=f'Cog {extension} has successfully been reloaded',
                                color=0x00ff00)
    reloadEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=reloadEmbed)


@client.command()
async def button(ctx):
    await ctx.send("Buttons!", components=[Button(label="Button", custom_id="button1")])


@client.event
async def on_button_click(interaction):
    await interaction.respond(content="Button Clicked")


@client.command()
async def select(ctx):
    await ctx.send(
        "Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="a"),
                    SelectOption(label="b", value="b"),
                ],
                custom_id="select1",
            )
        ],
    )


@client.event
async def on_select_option(interaction):
    await interaction.respond(content=f"{interaction.values[0]} selected!")


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        print(f'{filename[:-3]} has loaded!')

client.run(TOKEN)
