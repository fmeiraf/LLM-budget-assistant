import discord
import os
import dotenv

# from interactions import Client, Intents
# from interactions.ext import prefixed_commands
import interactions


dotenv.load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
CMD_PREFIX = ""

td_example = """
Date
	
Transaction Description

Debit
	
Credit
	Balance
May 13, 2023	REEFTECHNOLOGY.COM	$13.00		$1,448.32
May 13, 2023	ABC*ANYTIME FITNESS	$28.34		$1,435.32
May 8, 2023	GOOGLE*YOUTUBEPREMIUM	$12.59		$227.48
May 7, 2023	Spotify P22E958E88	$16.79		$214.89
May 4, 2023	KOODO MOBILE PAC	$112.82		$198.10
Apr 30, 2023	GITHUB, INC.	$14.01		$85.28
Apr 29, 2023	ABC*ANYTIME FITNESS	$28.34		$71.27
Apr 27, 2023	SQUARE ONE INSURANCE SERV	$21.95		$42.93
Apr 26, 2023	CRAVE	$20.98		$20.98
Apr 20, 2023	ateteu	$123.1		$0.00
Apr 25, 2023	PAYMENT - THANK YOU		$2,285.05	$0.00


"""

from transaction_parser import parse_transactions
from rich import print as rprint

rprint(parse_transactions(td_example))
# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f"Logged in as {self.user} (ID: {self.user.id})")
#         print("------")

#     def is_bot_own_message(self, message):
#         # we do not want the bot to reply to itself
#         return message.author.id == self.user.id

#     async def on_message(self, message):
#         # we do not want the bot to reply to itself
#         if self.is_bot_own_message(message):
#             return

#         # health check
#         if message.content.startswith("hello"):
#             await message.reply("Hello!", mention_author=True)

#         if message.content.startswith("insert"):
#             pass  # add to db

#         if message.content.startswith("delete"):
#             pass  # delete from db

#         if message.content.startswith("update"):
#             pass  # update db


# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)
# client.run(BOT_TOKEN)
