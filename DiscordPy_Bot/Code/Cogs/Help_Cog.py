import discord
from discord.ext import commands


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            helpEmbed = discord.Embed(description=page)
            await destination.send(embed=helpEmbed)

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            # U+2002 Middle Dot
            joined = '\u2002'.join(c.name for c in commands)
            if heading.endswith("_Cog"):
                self.paginator.add_line(f'**{heading[:-4]}**')
            else:
                self.paginator.add_line(f'**{heading}**')

            self.paginator.add_line(joined)


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
