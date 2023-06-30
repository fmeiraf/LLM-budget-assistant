import discord
from discord.ext import commands
import abc
from dotenv import load_dotenv
from transaction_parser import TransactionParser


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
        self.followup_message_id = None

    def is_bot_own_message(self, message):
        return message.author.id == self.bot.user.id

    def update_last_message_id(self, message):
        self.last_message_id = message.id

    @abc.abstractmethod
    async def starter_message(self, message):
        """First message sent when message content matches Cog trigger."""
        pass

    @abc.abstractmethod
    async def message_reply(self, message):
        """Message when user replies to bot starter message"""
        pass

    @abc.abstractmethod
    async def followup_reply(self, message):
        """Message when user replies to bot first reply message"""
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
        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        await message.channel.send("You replied to my message!")

    async def followup_reply(self, message):
        return

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


class Menu(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content=f"Hi {message.author.mention}  😎 \n \n Let's start working! What would you like to do now?\
            Chose between the options below: \n ",
            reference=message,
            view=MenuView(bot=self.bot),
        )
        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        await message.channel.send("You replied to my message!")

    async def followup_reply(self, message):
        return

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "menu":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                print(self.last_message_id, message.reference.message_id)
                await self.message_reply(message)

    def setup(bot):
        bot.add_cog(Menu(bot))


class AddTransaction(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Sure 💳! \nGrab the trasanction information from your account and send me a reply to this message"
            " (just copy and paste, easy like that)",
            reference=message,
        )
        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        # transaction_string = message.content
        # transaction_parser = TransactionParser(transaction_string)
        # parsed_transactions = transaction_parser.extract_transaction_info()
        await message.channel.send("You  have added  a new transaction $$ ")

    async def followup_reply(self, message):
        return

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
        bot.add_cog(AddTransaction(bot))


class AddAccount(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Be creatiave 👨‍🎨 !! \n"
            "Reply to this message with the name you want for your new account "
            "(you can choose anything like credit card, cc 4545, debit, mastercard, etc)",
            reference=message,
        )
        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        new_account = message.content

        # checking if new account name already exists
        if self.bot.db_client.get_account_id_by_name(
            user_id=self.bot.user_id, account_name=new_account
        ):
            await message.channel.send(
                f"Sorry, you already have a category with that name"
            )
            return
        else:
            self.bot.db_client.create_account(
                user_id=self.bot.user_id, account_name=new_account
            )
            await message.channel.send("You  have added  a new account $$  ")

            return

    async def followup_reply(self, message):
        return

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
        bot.add_cog(AddAccount(bot))


class LogIn(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Hey there 👋! \n Please reply to my message with your e-mail so I can find your profile.",
            reference=message,
        )

        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        user_id = self.bot.db_client.get_user_id_by_email(message.content)

        if user_id:
            self.bot.store_user_id(user_id)
            await message.channel.send(f"You are logged in now!")
        else:
            await message.channel.send(
                f"Sorry, I couldn't find any profile with that e-mail"
            )

    async def followup_reply(self, message):
        return

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "log in":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                await self.message_reply(message)

    def setup(bot):
        bot.add_cog(LogIn(bot))


class SignUp(MessageInteraction):
    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content="Ok ok let's get you up and running👋! \n Provide me with an e-mail so I can create you a profile.",
            reference=message,
        )

        self.update_last_message_id(starter_message)

    async def message_reply(self, message):
        email = message.content
        user_id = self.bot.db_client.create_user(
            email, "password"
        )  # password via chat doesn't make sense, will change later

        self.bot.store_user_id(user_id)

        if user_id:
            await message.channel.send(f"Your profile has been created!")
        else:
            await message.channel.send(
                f"Sorry, I couldn't create your profile. Please try again later"
            )

    async def followup_reply(self, message):
        return

    @commands.Cog.listener("on_message")
    async def message_router(self, message):
        if self.is_bot_own_message(message):
            return
        else:
            if message.content.lower() == "sign up":
                await self.starter_message(message)
            elif (
                message.reference
                and self.last_message_id == message.reference.message_id
            ):
                await self.message_reply(message)
            elif (
                message.reference
                and self.followup_message_id == message.reference.message_id
            ):
                await self.followup_reply(message)

    def setup(bot):
        bot.add_cog(SignUp(bot))


cogs = [Menu, Greetings, AddTransaction, AddAccount, LogIn, SignUp]


## __VIEWS__ ##


class GreetingsView(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(
        label="Log In",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji="▶️",
    )
    async def first_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        LogIn_instance = self.bot.get_cog("LogIn")

        await LogIn_instance.starter_message(interaction.message)
        await interaction.response.defer()  # this is to avoid interaction fail in the UI

    @discord.ui.button(
        label="Sign Up", row=0, style=discord.ButtonStyle.green, emoji="➕"
    )
    async def second_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        SignUp_instance = self.bot.get_cog("SignUp")

        await SignUp_instance.starter_message(interaction.message)
        await interaction.response.defer()  # this is to avoid interaction fail in the UI


class MenuView(
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
