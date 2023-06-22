import discord
from discord.ext import commands
import abc
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file


## __COGS__ ##


class CustomMeta(abc.ABCMeta, type(commands.Cog)):
    pass


class MessageInteraction(commands.Cog, metaclass=CustomMeta):
    """
    Abstract class for message interaction cogs.

    "Cog trigger" in this context means the content of the message that will trigger the Cog to run.
    Each MessageInteraction Cog will listen for specific messages contents and respond to it accordingly.
    Cogs will also isolate specific actions the user could do like, insert things, ask for help, etc.

    Every cog has its own state to keep track of the last message sent by the bot
    this way user can interact with these messages and get specific actions/responses

    """

    def __init__(self, bot):
        self.bot = bot
        self.last_message_id = None
        self.is_auto_start = False  #

        if self.is_auto_start:
            self.auto_start()

    def is_bot_own_message(self, message):
        return message.author.id == self.bot.user.id

    @abc.abstractmethod
    async def starter_message(self, message):
        """First message sent when message content matches Cog trigger."""
        pass

    @abc.abstractmethod
    async def message_reply(self, message):
        """Message when user replies to bot starter message"""
        pass

    @abc.abstractmethod
    async def message_router(self, message):
        """Routes message to appropriate function based on content."""
        pass

    def setup(bot):
        bot.add_cog(MessageInteraction(bot))


class Greetings(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content=f"Hi {message.author.mention}  😎 \n \n Let's start working! What would you like to do now?\
            Chose between the options below: \n ",
            reference=message,
            view=GreetingsView(bot=self.bot),
        )
        self.last_message_id = starter_message.id

    async def message_reply(self, message):
        await message.channel.send("You replied to my message!")

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "hello":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                print(self.last_message_id, message.reference.message_id)
                await self.message_reply(message)

    def setup(bot):
        bot.add_cog(Greetings(bot))


class AddTransaction(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Be creatiave 👨‍🎨 !! \n"
            "Reply to this message with the name you want for your new account "
            "(you can choose anything like credit card, cc 4545, debit, mastercard, etc)",
            reference=message,
        )
        self.last_message_id = starter_message.id

    async def message_reply(self, message):
        await message.channel.send("You  have added  a new transaction $$ ")

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "add transaction":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                await self.message_reply(message)

    def setup(bot):
        bot.add_cog(Greetings(bot))


class AddAccount(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Sure 💳! \nGrab the trasanction information from your account and send me a reply to this message"
            " (just copy and paste, easy like that)",
            reference=message,
        )
        self.last_message_id = starter_message.id

    async def message_reply(self, message):
        await message.channel.send("You  have added  a new account $$ ")

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "add account":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                await self.message_reply(message)

    def setup(bot):
        bot.add_cog(Greetings(bot))


cogs = [Greetings, AddTransaction, AddAccount]


## __VIEWS__ ##


class GreetingsView(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(
        label="Add new account",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji="💳",
    )
    async def first_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        AddTransaction_instance = self.bot.get_cog("AddAccount")

        await AddTransaction_instance.starter_message(interaction.message)
        await interaction.response.defer()  # this is to avoid interaction fail in the UI

    @discord.ui.button(
        label="Add transactions", row=0, style=discord.ButtonStyle.secondary, emoji="💸"
    )
    async def second_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        AddTransaction_instance = self.bot.get_cog("AddTransaction")

        await AddTransaction_instance.starter_message(interaction.message)
        await interaction.response.defer()  # this is to avoid interaction fail in the UI
