from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import client


class Utility_Cog(commands.Cog):
    """This is the utility cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Current ping is: {round(client.latency * 1000)}ms')


def setup(bot):
    bot.add_cog(Utility_Cog(bot))
