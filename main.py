import discord
from player import player


# create a Discord client instance
intents = discord.Intents.all()
# intents.members = True
client = discord.Client(intents=intents)
players = {}


# define the bot command
@client.event
async def on_message(message):
    print(message.content)
  # check if the message is from the bot or not
    if message.author == client.user:
        return
  # check if the message has a valid command
    if message.content[0:len("!p")] == "!p":
    # get the URL of the video from the command
        search_query = message.content[len("!p "):]

    # # create a voice client
        try:
            queue_item = players[message.guild.id].add_to_queue(search_query)

        except KeyError:
            voice_channel = message.author.voice.channel
            vc = await voice_channel.connect()
            players[message.guild.id] = player(client.voice_clients[-1])
            queue_item = players[message.guild.id].add_to_queue(search_query)

        if queue_item.print_url:
            await message.channel.send("🎶 " + queue_item.title + " was added to the queue.\n" + queue_item.url)
        else:
            await message.channel.send("🎶 " + queue_item.title + " was added to queue.")
        
        if players[message.guild.id].is_playing != True:
            await players[message.guild.id].play()


    if message.content[0:len("!l")] == "!l":
        try:
            await players[message.guild.id].voice_channel.disconnect()
            del players[message.guild.id]
        
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

    if message.content[0:len("!pause")] == "!pause":
        try:
            await players[message.guild.id].voice_channel.pause()
        
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

    if message.content[0:len("!resume")] == "!resume" :
        try:
            await players[message.guild.id].voice_channel.resume()
        
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

    if message.content[0:len("!s")] == "!s":
        try:
            await players[message.guild.id].skip()

            # using current_queue - 1 because the removal of the skipped item only
            # happens in a new thread (is triggered in vc.play(after:lambda e:))
            # therefore, to get the newest item, we have to move one ahead for the message.

            if len(players[message.guild.id].current_queue) - 1 > 0:
                response = "🎶 NOW PLAYING: " + players[message.guild.id].current_queue[1].title
                await message.channel.send(response)


        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")
    
    if message.content[0:len("!q")] == "!q":
        try:
            print("oh yeah yeah")
            response = "Current items in queue: 📋\n"
            for item in players[message.guild.id].current_queue:
                response += item.title + "\n" 
            await message.channel.send(response)
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

    if message.content[0:len("!ai")] == "!ai":
        message.content = message.content[len("!ai"):]
        
        if len(message.content > 1500):
            await message.channel.send("That message is too big cuh.")
            return
        
        try:
        
            await players[message.guild.id].play_ai(message)
        
        except KeyError:
            
            voice_channel = message.author.voice.channel
            vc = await voice_channel.connect()
            players[message.guild.id] = player(client.voice_clients[-1])
            
            await players[message.guild.id].play_ai(message)


# start the Discord bot
client.run("OTE0MzYyMjE1OTU0NTQ2NzQ4.GDZu-G.4OJnBypG8kVUHcfzyeW3QyP7VAGFNQj8hTTims", log_handler=None)