from discord.message import Message
from discord import VoiceClient
from router import router
from player import player

players: dict[str, player] = {}

@router.command('!p')
async def play(var, message: Message):
    song_req, = var
    try:
        queue_item = players[message.guild.id].add_to_queue(song_req)

    except KeyError:
        voice_channel = message.author.voice
        
        if voice_channel != None:
            vc = await voice_channel.channel.connect()
            if type(vc) == VoiceClient:
                players[message.guild.id] = player(vc)
                queue_item = players[message.guild.id].add_to_queue(song_req)
        
        else:
            await message.channel.send(':rage: Unable to join VC :rage:')
            return 

    if queue_item.print_url:
        await message.channel.send("🎶 " + queue_item.title + " was added to the queue.\n" + queue_item.url)
    else:
        await message.channel.send("🎶 " + queue_item.title + " was added to queue.")
    
    if players[message.guild.id].is_playing == False:
        await players[message.guild.id].play()
    
@router.command('!l')
async def leave(var, message: Message):
    try:
        await players[message.guild.id].voice_channel.disconnect()
        del players[message.guild.id]
    
    except KeyError:
        await message.channel.send("Dipshit im not even in a channel yet.")


@router.command("!pause")
async def pause(var, message: Message):
    if message.content[0:len("!pause")] == "!pause":
        try:
            players[message.guild.id].voice_channel.pause()
        
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")


@router.command('!resume')
async def resume(var, message: Message):
    if message.content[0:len("!resume")] == "!resume" :
        try:
            players[message.guild.id].voice_channel.resume()
        
        except KeyError:
            await message.channel.send("Dipshit im not even in a channel yet.")

@router.command("!s")
async def skip(var, message: Message):
    try:
        index, = var
        
    except:
        index = 0

    try:
        response = "Skipped ⏭️"
        if len(players[message.guild.id].current_queue) - 1 > 0:

            response += "🎶 NOW PLAYING: " + players[message.guild.id].current_queue[1].title
            await message.channel.send(response)
        await message.channel.send(response)
        players[message.guild.id].skip()

    except KeyError:
        await message.channel.send("Dipshit im not even in a channel yet.")