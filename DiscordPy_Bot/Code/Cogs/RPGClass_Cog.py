import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import cursor, connection, client

classList = ['Knight', 'Rogue', 'Mage', 'Ranger']
classEmoji = ['⚔️', '🗡️', '🔮', '🏹']
confirmEmoji = ['✅', '◀️']
emojiIndex = 0
classDescriptions = ['Knight description', 'Rogue description', 'Mage description', 'Ranger Description']
descriptionIndex = 0


class RPGClass_Cog(commands.Cog):
    """This is the character classes category"""

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

        embedClass = discord.Embed(title='Choose your starting class',
                                   description='Pick your first character wisely', )
        for classField in classList:
            embedClass.add_field(name=await self.embedEmoji() + ' ' + classField + ' ' + await self.embedEmoji(),
                                 value=await self.embedDescription(), inline=True)
            emojiIndex += 1
            descriptionIndex += 1
        embedClass.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        embedClass.set_thumbnail(url=ctx.author.avatar_url)
        embedClass.set_footer(text='Reacting with a specific class emoji will let you see a detailed description.'
                                   '\nYou will be able to create another character later on')

        embedMessage = await ctx.send(embed=embedClass)

        async def repeat():
            await embedMessage.edit(embed=embedClass)

            for reactions in classEmoji:
                await embedMessage.add_reaction(reactions)

            emojiIndex = 0
            descriptionIndex = 0

            def checkFirstEmbed(reaction, user):
                return user == ctx.author and str(reaction.emoji) in classEmoji

            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=checkFirstEmbed)
            await embedMessage.clear_reactions()

            # After reacting, clear reactions and send second embed

            global pickedClass

            if str(reaction.emoji) == '⚔️':
                knightEmbed = discord.Embed(title='⚔️ Knight ⚔️', description='Knight description', color=0x00ff00)
                knightEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                knightEmbed.set_thumbnail(url=ctx.author.avatar_url)
                knightEmbed.set_footer(text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                await embedMessage.edit(embed=knightEmbed)
                await embedMessage.add_reaction('◀️')
                await embedMessage.add_reaction('✅')
                pickedClass = 'Knight'

            elif str(reaction.emoji) == '🗡️':
                rogueEmbed = discord.Embed(title='🗡️ Rogue 🗡️', description='Rogue description', color=0x00ff00)
                rogueEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                rogueEmbed.set_footer(text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                await embedMessage.edit(embed=rogueEmbed)
                await embedMessage.add_reaction('◀️')
                await embedMessage.add_reaction('✅')
                pickedClass = 'Rogue'

            elif str(reaction.emoji) == '🔮':
                mageEmbed = discord.Embed(title='🔮 Mage 🔮', description='Mage description', color=0x00ff00)
                mageEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                mageEmbed.set_footer(text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                await embedMessage.edit(embed=mageEmbed)
                await embedMessage.add_reaction('◀️')
                await embedMessage.add_reaction('✅')
                pickedClass = 'Mage'

            elif str(reaction.emoji) == '🏹':
                rangerEmbed = discord.Embed(title='🏹 Ranger 🏹', description='Ranger description', color=0x00ff00)
                rangerEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                rangerEmbed.set_footer(text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                await embedMessage.edit(embed=rangerEmbed)
                await embedMessage.add_reaction('◀️')
                await embedMessage.add_reaction('✅')
                pickedClass = 'Ranger'

            def checkSecondEmbed(reactionConfirm, userConfirm):
                return userConfirm == ctx.author and str(reactionConfirm.emoji) in confirmEmoji

            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=checkSecondEmbed)

            await embedMessage.clear_reactions()

            if str(reaction.emoji) == '✅':
                lastEmbed = discord.Embed(title='Congratulations!',
                                          description=f'You are now a **{pickedClass}** and can continue onto your '
                                                      'adventure! Please use **mmo help** to see more commands!',
                                          color=0x00ff00)
                lastEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                await embedMessage.edit(embed=lastEmbed)
                cursor.execute(
                    f'INSERT INTO Players (PlayerName, PlayerID) VALUES("{ctx.message.author.name}", "{ctx.message.author.id}")')
                connection.commit()
            elif str(reaction.emoji) == '◀️':
                await repeat()

        emojiIndex = 0
        descriptionIndex = 0
        await repeat()


def setup(bot):
    bot.add_cog(RPGClass_Cog(bot))
