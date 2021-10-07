import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import categoryFields
from DiscordPy_Bot.Code.HelpRegistry import *


class Help_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    RegisterCategory(commands.Cog.__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def Help(self, ctx):
        RegisterCommand(self.__name__)
        if category is not None and command is None:
            CategoryHelp()
        elif category is None and command is not None:
            CommandHelp()
        elif category is not None and command is not None:
            CommandHelp()
        elif category is None and command is None:

            embedVar = discord.Embed(title="Commands",
                                     description="Prefix: **mmo** \n For more info: **mmo help [command/category]**",
                                     color=0x00ff00)

            for field in categoryFields:
                embedVar.add_field(name=field, value="a", inline=False)
            await ctx.channel.send(embed=embedVar)


# register category
# register command using __name__
# tell difference between the two
# make embed value list of category commands
def setup(bot):
    bot.add_cog(Help_Cog(bot))
