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

    # mmo help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help', description='For more info on a category, use **mmo** help `<category>`'
                                                        '\nFor more info on a command use **mmo** help `<command>`')
        for groupName in groups:
            embed.add_field(name=f'**{groupName}**', value="a", inline=False)
        await self.context.send(embed=embed)

    # mmo help <command>
    async def send_command_help(self, command):
        embedCommandHelp = discord.Embed(title=str(command) + " command:", description=command.short_doc)
        await self.context.send(embed=embedCommandHelp)

    # mmo help <group>
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
