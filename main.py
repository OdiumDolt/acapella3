import discord
from router import router
import commands.music
import os


TOKEN = os.getenv('DISCORD')

# create a Discord client instance
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# define the bot command
@client.event
async def on_message(message: discord.message.Message):
    # check if the message is from the bot or not
    if message.author == client.user:
        return
    try:
        func, args = router.find(message.content)
        await func(args, message)
    except:
        pass
        

# start the Discord bot
client.run(TOKEN)