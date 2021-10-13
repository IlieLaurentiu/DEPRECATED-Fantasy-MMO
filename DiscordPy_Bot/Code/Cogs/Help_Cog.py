import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import groups

attributes = {
    'name': "hell",
    'aliases': ["help", "helps"],
    'cooldown': commands.Cooldown(2, 5.0, commands.BucketType.user)
}

help_object = commands.MinimalHelpCommand(command_attrs=attributes)


class MyNewHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

    # !help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help')
        for groupName in groups:
            embed.add_field(name=f'**{groupName}**', value="a", inline=False)
        await self.context.send(embed=embed)

    # !help <command>
    async def send_command_help(self, command):
        await self.context.send("This is help command")

    # !help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")


class Help_Cog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyNewHelp()
        bot.help_command.cog = self

    @commands.Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(Help_Cog(bot))
