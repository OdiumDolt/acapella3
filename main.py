import discord
from player import player
import json
import router
import commands.music
ENVIRON = "PROD"

# create a Discord client instance
intents = discord.Intents.all()
# intents.members = True
client = discord.Client(intents=intents)
players: dict[str, player] = {}


with open('token.json', "r") as read_file:
    file = json.load(read_file)

TOKEN = file[ENVIRON]


# define the bot command
@client.event
async def on_message(message: discord.message.Message):
    # check if the message is from the bot or not
    if message.author == client.user:
        return
    
    func, args = router.router.find(message.content)
    await func(args, message)

# start the Discord bot
client.run(TOKEN)
