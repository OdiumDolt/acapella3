from discord.message import Message
from discord import VoiceClient
from router import router
from player import player
import random


players: dict[str, player] = {}

def playerExists(id: int) -> bool:
    try:
        players[id]
        return True
    except KeyError:
        return False

async def createPlayerIfNoneExists(message: Message) -> player:
    if playerExists(message.guild.id):
        return players[message.guild.id]
    
    voice_channel = message.author.voice
    if voice_channel == None:
        await message.channel.send(':rage: Unable to join Voice Channel :rage:')
        raise KeyError
    
    else:
        vc = await voice_channel.channel.connect()
        if type(vc) == VoiceClient:
            newPlayer = player(vc)
            players[message.guild.id] = newPlayer
            return newPlayer
        else:
            print('type wasnt VoiceClient')
            raise KeyError

@router.command('!p')
async def play(var: str, message: Message):
    song_req, = var
    current_player = await createPlayerIfNoneExists(message)
    
    
    if "youtube.com/playlist" in song_req:
        print('PLAYLIST DETECTED')
        return

    queue_item = current_player.add_to_queue(song_req)

    if queue_item.print_url:
        await message.channel.send("🎶 " + queue_item.title + " was added to the queue.\n" + queue_item.url)
    else:
        await message.channel.send("🎶 " + queue_item.title + " was added to queue.")
    
    if players[message.guild.id].is_playing == False:
        await players[message.guild.id].play()
    
@router.command("!q")
async def queue(var, message: Message):
    current_player = await createPlayerIfNoneExists(message)
    response = ""
    for queue in range(len(current_player.current_queue)):
        if queue == 0:
            response += "🎶 " + current_player.current_queue[queue].title + "\n"
            continue
        response += current_player.current_queue[queue].title + "\n"
        
    await message.channel.send(response)
            

@router.command('!l')
async def leave(var, message: Message):
    current_player = await createPlayerIfNoneExists(message)
    await current_player.voice_channel.disconnect()
    del players[message.guild.id]


@router.command("!pause")
async def pause(var, message: Message):
    current_player = await createPlayerIfNoneExists(message)
    
    current_player.voice_channel.pause()


@router.command('!resume')
async def resume(var, message: Message):
        current_player = await createPlayerIfNoneExists(message)
        current_player.voice_channel.resume()

@router.command("!s")
async def skip(var, message: Message):
    current_player = await createPlayerIfNoneExists(message)
    
    response = "Skipped ⏭️\n"
    
    if len(current_player.current_queue) - 1 > 0:
        response += "🎶 NOW PLAYING: " + current_player.current_queue[1].title
    
    await message.channel.send(response)
    
    current_player.skip()

@router.command('!shuffle')
async def shuffle(var, message: Message):
    current_player = await createPlayerIfNoneExists(message)

    if len(current_player.current_queue) > 0:
        song = current_player.current_queue.pop(0)
        random.shuffle(current_player.current_queue)
        current_player.current_queue.insert(0, song)
        await queue(var, message)
            

@router.command("!duration")
async def duration(var: str | None, message: Message):
    current_player = await createPlayerIfNoneExists(message)
    progress = current_player.voice_channel.source.progress
    duration = current_player.voice_channel.source.duration

    await message.channel.send(str(progress) + "s / " + str(duration) + "s")