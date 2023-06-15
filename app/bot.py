import discord
import os  # default module
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file


class BotClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    def is_bot_own_message(self, message):
        # we do not want the bot to reply to itself
        return message.author.id == self.user.id

    async def starter_message(self, message):
        starter_message = await message.channel.send(
            content=f"Hi {message.author.mention}  😎 \n \n Let's start working! What would you like to do now? Chose between the options below: \n ",
            reference=message,
            view=StarterView(),
        )
        self.starter_message_id = starter_message.id
        return starter_message

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if self.is_bot_own_message(message):
            return

        if message.content == "hi":
            await self.starter_message(message)

        if (
            message.reference
            and message.reference.message_id == self.starter_message_id
        ):
            await message.channel.send("tuche")


class StarterView(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(
        label="Add transactions",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji="💸",
    )
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(
        label="Update transactions", row=0, style=discord.ButtonStyle.secondary, emoji="🔄"
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")


# bot = discord.Bot(intents=intents)
intents = discord.Intents.default()
intents.message_content = True
bot = BotClient(intents=intents)
bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # run the bot with the token
