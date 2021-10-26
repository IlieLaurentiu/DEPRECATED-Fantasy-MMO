import discord
from discord.ext import commands
from DiscordPy_Bot.Code.MainClient import cursor, connection, client


classList = ['Knight', 'Rogue', 'Mage', 'Ranger']
classEmoji = ['⚔️', '🗡️', '🔮', '🏹']
confirmEmoji = ['✅', '◀️']
classDescriptions = ['Knight description', 'Rogue description', 'Mage description', 'Ranger Description']

client.emojiIndex = 0
client.descriptionIndex = 0
client.pickedClass = ''


class RPGClass_Cog(commands.Cog):
    """Character related cog"""

    async def EmbedEmoji(self):
        return classEmoji[client.emojiIndex]

    async def EmbedDescription(self):
        return classDescriptions[client.descriptionIndex]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def Start(self, ctx):
        """The start command will allow you to pick your first character and unlock the rest of the commands"""

        cursor.execute(f'SELECT PlayerID FROM Players WHERE PlayerID = {ctx.author.id}')
        playerID = cursor.fetchone()
        print(playerID)
        print(ctx.author.id)

        if playerID is None:
            # Send the Character Selection Embed
            selectionEmbed = discord.Embed(title='Choose your starting class',
                                           description='Here you will create your first character! Pick your starting class.', )
            for classField in classList:
                selectionEmbed.add_field(
                    name=await self.EmbedEmoji() + ' ' + classField + ' ' + await self.EmbedEmoji(),
                    value=await self.EmbedDescription(), inline=True)
                client.emojiIndex += 1
                client.descriptionIndex += 1
            selectionEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            selectionEmbed.set_thumbnail(url=ctx.author.avatar_url)
            selectionEmbed.set_footer(
                text='Reacting with a specific emoji will let you see a detailed description of that class without having to pick it.'
                     '\nYou will be able to create multiple characters with different classes')

            embedMessage = await ctx.send(embed=selectionEmbed)

            # Return point if the player goes back to selection embed
            async def Repeat():
                await embedMessage.edit(embed=selectionEmbed)

                for reactions in classEmoji:
                    await embedMessage.add_reaction(reactions)

                client.emojiIndex = 0
                client.descriptionIndex = 0

                def checkFirstEmbed(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in classEmoji

                # Send and wait for the first embed
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=checkFirstEmbed)
                    await embedMessage.clear_reactions()

                    if reaction.emoji == '⚔️':
                        knightEmbed = discord.Embed(title='⚔️ Knight ⚔️', description='Knight description',
                                                    color=0x00ff00)
                        knightEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                        knightEmbed.set_thumbnail(url=ctx.author.avatar_url)
                        knightEmbed.set_footer(
                            text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                        await embedMessage.edit(embed=knightEmbed)
                        await embedMessage.add_reaction('◀️')
                        await embedMessage.add_reaction('✅')
                        client.pickedClass = 'Knight'

                    elif str(reaction.emoji) == '🗡️':
                        rogueEmbed = discord.Embed(title='🗡️ Rogue 🗡️', description='Rogue description',
                                                   color=0x00ff00)
                        rogueEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                        rogueEmbed.set_footer(
                            text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                        await embedMessage.edit(embed=rogueEmbed)
                        await embedMessage.add_reaction('◀️')
                        await embedMessage.add_reaction('✅')
                        client.pickedClass = 'Rogue'

                    elif str(reaction.emoji) == '🔮':
                        mageEmbed = discord.Embed(title='🔮 Mage 🔮', description='Mage description', color=0x00ff00)
                        mageEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                        mageEmbed.set_footer(
                            text='React with ◀️to go back to selection \nReact with ✅ to confirm your class')
                        await embedMessage.edit(embed=mageEmbed)
                        await embedMessage.add_reaction('◀️')
                        await embedMessage.add_reaction('✅')
                        client.pickedClass = 'Mage'

                    elif str(reaction.emoji) == '🏹':
                        rangerEmbed = discord.Embed(title='🏹 Ranger 🏹', description='Ranger description',
                                                    color=0x00ff00)
                        rangerEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                        rangerEmbed.set_footer(
                            text='React with ◀️to go back to selection \nReact with ✅ to confirm pciking this class')
                        await embedMessage.edit(embed=rangerEmbed)
                        await embedMessage.add_reaction('◀️')
                        await embedMessage.add_reaction('✅')
                        client.pickedClass = 'Ranger'

                except TimeoutError:
                    timeoutEmbed = discord.Embed(title='Command timed out',
                                                 description='Time ran out. Please add a reaction within 5 minutes of starting the command.')
                    timeoutEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=timeoutEmbed)

                def checkSecondEmbed(reactionConfirm, userConfirm):
                    return userConfirm == ctx.author and str(reactionConfirm.emoji) in confirmEmoji

                # Send and wait for the second embed
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=checkSecondEmbed)

                    await embedMessage.clear_reactions()
                    if str(reaction.emoji) == '✅':
                        lastEmbed = discord.Embed(title='Congratulations!',
                                                  description=f'You have picked a **{client.pickedClass}** character and can now continue onto your '
                                                              'adventure! Please use **mmo help** to see more commands!',
                                                  color=0x00ff00)
                        lastEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                        await embedMessage.edit(embed=lastEmbed)

                        cursor.execute(
                            f"""INSERT INTO Players (
                            PlayerName, PlayerID, CurrentCharacter, MaxCharacters, CharacterSlots, Level, Experience, Gold, Vitality, MaxVit, ManaPoints,
                            MaxMana, Defense, Attack, Intelligence, Evasion ) 
                            VALUES("{ctx.message.author.name}", "{ctx.message.author.id}", "{client.pickedClass}", "{1}", "{1}", "{1}", "{0}", "{100}",
                            {250}, {250}, {300}, {300}, {0}, {10}, {2}, {0}
                            )""")
                        connection.commit()
                    elif str(reaction.emoji) == '◀️':

                        await Repeat()

                except TimeoutError:
                    secondTimeoutEmbed = discord.Embed(title='Command timed out',
                                                       description='Time ran out. Please add a reaction within 5 minutes of starting the command.')
                    secondTimeoutEmbed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=secondTimeoutEmbed)

            client.emojiIndex = 0
            client.descriptionIndex = 0
            await Repeat()

        else:
            embed_didStart = discord.Embed(name='You already started',
                                           description='You already have confirmed your class and used this command once.'
                                                       '\n Please use **mmo help** to see all commands!'
                                           , color=0x00ff00)
            embed_didStart.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed_didStart)

    @commands.command(aliases=['p'])
    async def Profile(self, ctx):
        cursor.execute(f'SELECT * FROM Players WHERE PlayerID = {ctx.author.id}')
        statSheet = cursor.fetchone()

        profileEmbed = discord.Embed(title='Profile', description='All of your stats can be seen here', color=0x00ff00)

        profileEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        profileEmbed.add_field(name='Class', value=statSheet[2], inline=False)
        profileEmbed.add_field(name='Level', value=statSheet[5], inline=True)
        profileEmbed.add_field(name='Experience', value=statSheet[6], inline=False)
        profileEmbed.add_field(name='🪙 Gold', value=statSheet[7], inline=False)
        profileEmbed.add_field(name='❤️ VIT', value=statSheet[8], inline=True)
        profileEmbed.add_field(name=' 🔷 MP', value=statSheet[10], inline=True)
        profileEmbed.add_field(name='  🛡️ DEF', value=statSheet[12], inline=True)
        profileEmbed.add_field(name=' ⚔️ ATT', value=statSheet[13], inline=True)
        profileEmbed.add_field(name='🧠 INT', value=statSheet[14], inline=True)
        profileEmbed.add_field(name='EVA', value=statSheet[15], inline=True)

        await ctx.send(embed=profileEmbed)

def setup(bot):
    bot.add_cog(RPGClass_Cog(bot))
