from discord.message import Message
from discord import VoiceClient
from router import router
from player import player

players: dict[str, player] = {}

@router.command('!p')
async def play(var: str, message: Message):
    song_req, = var
    try:
        queue_item = players[message.guild.id].add_to_queue(song_req)

    except KeyError:
        voice_channel = message.author.voice
        
        if voice_channel == None:
            await message.channel.send(':rage: Unable to join VC :rage:')
            return
        else:
            vc = await voice_channel.channel.connect()
            if type(vc) == VoiceClient:
                players[message.guild.id] = player(vc)
                queue_item = players[message.guild.id].add_to_queue(song_req)

    if queue_item.print_url:
        await message.channel.send("🎶 " + queue_item.title + " was added to the queue.\n" + queue_item.url)
    else:
        await message.channel.send("🎶 " + queue_item.title + " was added to queue.")
    
    if players[message.guild.id].is_playing == False:
        await players[message.guild.id].play()
    
@router.command("!q")
async def queue(var, message: Message):
    try:
        current_player = players[message.guild.id]
    except KeyError:
        await message.channel.send('Not yet in a channel :sob:')
        return 
    response = ""
    for queue in range(len(current_player.current_queue)):
        if queue == 0:
            response += "🎶 " + current_player.current_queue[queue].title + "\n"
            continue
        response += current_player.current_queue[queue].title + "\n"
        
    await message.channel.send(response)
            

@router.command('!l')
async def leave(var, message: Message):
    try:
        await players[message.guild.id].voice_channel.disconnect()
        del players[message.guild.id]
    
    except KeyError:
        await message.channel.send("Not yet in a channel :sob:")


@router.command("!pause")
async def pause(var, message: Message):
    if message.content[0:len("!pause")] == "!pause":
        try:
            players[message.guild.id].voice_channel.pause()
        
        except KeyError:
            await message.channel.send("Not yet in a channel :sob:")


@router.command('!resume')
async def resume(var, message: Message):
    if message.content[0:len("!resume")] == "!resume" :
        try:
            players[message.guild.id].voice_channel.resume()
        
        except KeyError:
            await message.channel.send("Not yet in a channel :sob:")

@router.command("!s")
async def skip(var, message: Message):
    try:
        index, = var
        
    except:
        index = 0

    try:
        response = "Skipped ⏭️\n"
        if len(players[message.guild.id].current_queue) - 1 > 0:
            response += "🎶 NOW PLAYING: " + players[message.guild.id].current_queue[1].title
        await message.channel.send(response)
        players[message.guild.id].skip()

    except KeyError:
        await message.channel.send("Not yet in a channel :sob:")

@router.command("!duration")
async def duration(var: str | None, message: Message):
    try:
        progress = players[message.guild.id].voice_channel.source.progress
        duration = players[message.guild.id].voice_channel.source.duration

        await message.channel.send(str(progress) + "s / " + str(duration) + "s")

    except KeyError:
        await message.channel.send("And error occured :x:")