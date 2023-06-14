import os
import dotenv
from bot import BotClient
import discord


dotenv.load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = BotClient(intents=intents)
client.run(BOT_TOKEN)


# BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
# CMD_PREFIX = ""

# td_example = """
# Date

# Transaction Description

# Debit

# Credit
# 	Balance
# May 13, 2023	REEFTECHNOLOGY.COM	$13.00		$1,448.32
# May 13, 2023	ABC*ANYTIME FITNESS	$28.34		$1,435.32
# May 8, 2023	GOOGLE*YOUTUBEPREMIUM	$12.59		$227.48
# May 7, 2023	Spotify P22E958E88	$16.79		$214.89
# May 4, 2023	KOODO MOBILE PAC	$112.82		$198.10
# Apr 30, 2023	GITHUB, INC.	$14.01		$85.28
# Apr 29, 2023	ABC*ANYTIME FITNESS	$28.34		$71.27
# Apr 27, 2023	SQUARE ONE INSURANCE SERV	$21.95		$42.93
# Apr 26, 2023	CRAVE	$20.98		$20.98
# Apr 20, 2023	ateteu	$123.1		$0.00
# Apr 25, 2023	PAYMENT - THANK YOU		$2,285.05	$0.00


# """

# from transaction_parser import TransactionParser
# from rich import print as rprint

# td = TransactionParser(td_example)
# rprint(td.parse_transactions())
