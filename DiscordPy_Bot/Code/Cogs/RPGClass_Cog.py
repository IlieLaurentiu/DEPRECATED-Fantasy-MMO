import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import cursor

classList = ["Knight", "Rogue", "Mage"]
classEmoji = ["⚔️", "🗡️", "🔮"]
emojiIndex = 0
classDescriptions = ["Knight description", "Rogue description", "Mage description"]
descriptionIndex = 0

class RPGClass_Cog(commands.Cog):
    """This is the utility cog"""

    async def embedEmoji(self):
        global emojiIndex
        return classEmoji[emojiIndex]

    async def embedDescription(self):
        global descriptionIndex
        return classDescriptions[descriptionIndex]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def start(self, ctx):
        global emojiIndex
        global descriptionIndex

        # Send Embed
        embedClass = discord.Embed(title="Choose your starting class",
                                   description="Each class will play through the game differently",
                                   color=0x00ff00)
        for classField in classList:
            embedClass.add_field(name=await self.embedEmoji() + " " + classField + " " + await self.embedEmoji(),
                                 value=await self.embedDescription(), inline=False)
            emojiIndex += 1
            descriptionIndex += 1

        embedClass.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        embedClass.set_thumbnail(url=ctx.author.avatar_url)
        embedClass.set_footer(text="Reacting with a specific class emoji will let you see a detailed description."
                                   "\nYou will be able to create another class character later on")

        # cursor.execute(f'INSERT INTO Players (PlayerName, PlayerID, Whitelisted) VALUES("{ctx.message.author.name}", "{ctx.message.author.id}", "1")')
        await ctx.send(embed=embedClass)

        # Reset indexes
        emojiIndex = 0
        descriptionIndex = 0



def setup(bot):
    bot.add_cog(RPGClass_Cog(bot))
