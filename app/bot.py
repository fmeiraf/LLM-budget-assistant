import discord
import os  # default module
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.message_command(
    name="Get Message ID"
)  # creates a global message command. use guild_ids=[] to create guild-specific commands.
async def get_message_id(
    ctx, message: discord.Message
):  # message commands return the message
    await ctx.respond(f"Message ID: `{message.id}`")


@bot.event
async def on_message(message):
    if message.content == "hi":
        await message.channel.send("hello", reference=message)


bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # run the bot with the token
