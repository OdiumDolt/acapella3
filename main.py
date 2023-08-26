import discord
from player import player
import json
import router
import commands.music

# create a Discord client instance
intents = discord.Intents.all()
# intents.members = True
client = discord.Client(intents=intents)
players: dict[str, player] = {}

ENVIRON = "DEV"
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

    if message.content[0:len("!s")] == "!s":
        try:

            if len(players[message.guild.id].current_queue) - 1 > 0:
                response = "🎶 NOW PLAYING: " + players[message.guild.id].current_queue[1].title
                await message.channel.send(response)
            
            players[message.guild.id].skip()


        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")
    
    if message.content[0:len("!q")] == "!q":
        try:
            response = "Current items in queue: 📋\n"
            for item in players[message.guild.id].current_queue:
                response += item.title + "\n" 
            await message.channel.send(response)
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

    if message.content[0:len("!ai")] == "!ai":
        message.content = message.content[len("!ai"):]
        
        if len(message.content) > 1500:
            await message.channel.send("That message is too big cuh.")
            return
        
        try:
        
            await players[message.guild.id].play_ai(message)
        
        except KeyError:
            
            voice_channel = message.author.voice.channel
            vc = await voice_channel.connect()
            players[message.guild.id] = player(vc)
            
            await players[message.guild.id].play_ai(message)

# start the Discord bot
client.run(TOKEN)
