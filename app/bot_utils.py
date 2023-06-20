import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file


## __COGS__ ##


class StarterMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def is_bot_own_message(self, message):
        # we do not want the bot to reply to itself
        return message.author.id == self.user.id

    async def create_message(self, message):
        starter_message = await message.channel.send(
            content=f"Hi {message.author.mention}  😎 \n \n Let's start working! What would you like to do now? \
            Chose between the options below: \n ",
            reference=message,
            view=StarterView(),
        )
        self.starter_message_id = starter_message.id
        return starter_message

    @commands.Cog.listener("on_message")
    async def hello(self, message):
        if message.content.lower() == "hello":
            # await message.channel.send("Hello there!")
            await self.create_message(message)

    def setup(bot):
        """General cog loading."""
        bot.add_cog(StarterMessage(bot))


class RandomMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def hello(self, message):
        if message.content.lower() == "touche":
            await message.channel.send("Ha!")

    def setup(bot):
        """General cog loading."""
        bot.add_cog(RandomMessage(bot))


cogs = [StarterMessage, RandomMessage]


## __VIEWS__ ##


class StarterView(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(
        label="Add new account",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji="💳",
    )
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """ Be creatiave 💳 !! \
            \nReply to this message with the name you want for your new account (you can choose anything like credit card, cc 4545, debit, mastercard, etc)"""
        )

    @discord.ui.button(
        label="Add transactions", row=0, style=discord.ButtonStyle.secondary, emoji="💸"
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """Sure!  💳  Grab the trasanction information from your account and send me a reply to this message (just copy and paste, easy like that)"""
        )
