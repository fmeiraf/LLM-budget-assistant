import discord
import os  # default module
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file


class BotClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        if message.content == "hi":
            await message.channel.send(
                f"hello {message.author.mention}", reference=message
            )


# bot = discord.Bot(intents=intents)
intents = discord.Intents.default()
intents.message_content = True
bot = BotClient(intents=intents)
bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # run the bot with the token


# @bot.event
# async def on_ready():
#     print(f"{bot.user} is ready and online!")


# @bot.slash_command(name="hello", description="Say hello to the bot")
# async def hello(ctx):
#     await ctx.respond("Hey!")


# @bot.event
# async def on_message(message):
#     if message.content == "hi":
#         await message.channel.send("hello", reference=message)
