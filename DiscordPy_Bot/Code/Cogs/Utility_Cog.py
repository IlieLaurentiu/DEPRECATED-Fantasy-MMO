import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import client, cursor, connection


class Utility_Cog(commands.Cog):
    """This is the utility cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    @commands.is_owner()
    async def Stats(self, ctx):
        for guild in client.guilds:
            client.guildCount += 1
            print(guild.name)
        statsEmbed = discord.Embed(name='Bot Stats:', description='Displays all the stats of the bot', color=0x00ff00)
        statsEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        statsEmbed.add_field(name='Guild Count:', value=client.guildCount, inline=True)
        await ctx.send(embed=statsEmbed)

    @commands.command()
    @commands.is_owner()
    async def dbtoconsole(self, ctx):
        cursor.execute(f'SELECT * FROM Players')
        connection.commit()
        print(cursor.fetchall())

    @commands.command()
    @commands.is_owner()
    async def resetPlayersDB(self, ctx):
        cursor.execute('DROP TABLE Players')
        connection.commit()
        print(cursor.fetchall())

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Current ping is: {round(client.latency * 1000)}ms')


def setup(bot):
    bot.add_cog(Utility_Cog(bot))
