import discord
from discord.ext import commands
import os  # default module
from dotenv import load_dotenv
from typing import List
from bot_utils import cogs

load_dotenv()  # load all the variables from the env file


class Bot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"{self.user} is ready and online!")


def start_bot(command_prefix="!", cogs_list: List[commands.Cog] = None):
    # INSTANTIATE BOT
    intents = discord.Intents.default()
    intents.message_content = True
    # bot = discord.Bot(command_prefix="!", intents=intents) #this is for when instantiating as class was problmatic
    bot = Bot(command_prefix="!", intents=intents)

    # ADD FUNCTIONALITY TO BOT USING COGS
    if cogs_list:
        for cog in cogs_list:
            bot.add_cog(cog(bot))

    bot.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    start_bot(cogs_list=cogs)
