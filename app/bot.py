import discord
import os
import dotenv

# import interactions


dotenv.load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
CMD_PREFIX = ""


class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    def is_bot_own_message(self, message):
        # we do not want the bot to reply to itself
        return message.author.id == self.user.id

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if self.is_bot_own_message(message):
            return

        # health check
        if message.content.startswith("hello"):
            await message.reply("Hello!", mention_author=True)

        if message.content.startswith("insert"):
            pass  # add to db

        if message.content.startswith("delete"):
            pass  # delete from db

        if message.content.startswith("update"):
            pass  # update db
