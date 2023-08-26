import re
import yt_dlp
import discord
import urllib
import asyncio
import pyttsx3
import os
import time


class player:
    def __init__(self, voice_channel: discord.VoiceClient) -> None:
        self.current_queue = []
        self.current_playing_thread = None
        self.voice_channel = voice_channel
        self.connected_guild = None
        self.is_playing = False
        self.last_play = None
   
    """
    Uses yt_dlp to extract data from youtube, specificly the stream_url (i_url),
    the stream_title, and the actual url.

    The actual url is gotten  get_url_from_search if the requested url is not in fact, a url.
    """
    def add_to_queue(self, url):
        
        print_url = False
        got_from = "url"
        
        if self.is_url(url) == None:
            url = self.get_url_from_search(url)
            print_url = True
            got_from = "search"
        
        # Use yt_dlp to extract the youtube videos information.
        ytdlp_opts = {'format': 'bestaudio/best', 'noplaylist':'False'}
        with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
            info = ytdl.extract_info(url, download=False)
            stream_url = info["url"]
            stream_title = info['fulltitle']
            

        # create the new queue_item object
        new_queue = queue_item(url, stream_title, print_url, got_from, stream_url)

        self.current_queue.append(new_queue)

        return new_queue


    """
    uses urllib to get the the html of a youtube search query. Basically the same as
    searching through a browser. Then uses regex to find the first youtube url (the first result)
    """
    def get_url_from_search(self, query):
        url_or_term = query.replace(" ", "+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url_or_term)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        
        return url


    """
    Checkes if a query is a youtube url. Thanks stackoverflow.
    """
    def is_url(self, search_query):
        return re.search("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", search_query)
    

    """
    Using self.voice_channel.stop() triggers the after callback found in self.play().
    This then triggers play_next, which pops the current_queue, and triggers self.play again()
    """
    def skip(self):
        self.voice_channel.stop()
    

    """
    handles playing the next song, only if the their is another song to play
    """
    async def play_next(self):
        self.current_queue.pop(0)
        if len(self.current_queue) == 0:
            self.is_playing = False
            return
        await self.play()


    """
    grabs the latest queue_item from self.current_queue and streams it from youtube

    discord.FFmpegOpusAudio.from_probe needs a streamable url, which is i_url
    
    the after callback runs play_next after the audio has finished playing
    """
    async def play(self):
        self.is_playing = True
        self.last_play = time.time()
        ffmpeg_opts = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}
        source = await discord.FFmpegOpusAudio.from_probe(self.current_queue[0].i_url, **ffmpeg_opts)
        self.voice_channel.play(source, after= lambda e:asyncio.run_coroutine_threadsafe(self.play_next(), self.voice_channel.loop))


    """"
    creates a pyttsx3 engine object, and sythisizes the audio.
    
    it then saves the audio to a file, and plays that through discord.FFmpegOpudAudio.from_probe
    
    the after callback just deletes the created file (speach.mp3)
    """
    async def play_ai(self, message):
        if self.is_playing:
            return
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 133) 
        engine.save_to_file(message.content, './' + str(message.guild.id) + '_speech.mp3')
        engine.runAndWait()
        
        source = await discord.FFmpegOpusAudio.from_probe(str(message.guild.id) + '_speech.mp3')
        self.voice_channel.play(source, after=lambda e: os.remove("./" + str(message.guild.id) + '_speech.mp3'))


class queue_item:
    def __init__(self, url, title, print_url, got_from, i_url) -> None:
        self.url = url
        self.title = title
        self.print_url = print_url
        self.got_from = got_from
        self.i_url = i_url