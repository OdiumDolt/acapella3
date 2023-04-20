import re
import yt_dlp
import discord
import urllib
import asyncio
import pyttsx3
import os
class player:

    def __init__(self, voice_channel) -> None:
        self.current_queue = []
        self.current_playing_thread = None
        self.voice_channel = voice_channel
        self.connected_guild = None
        self.is_playing = False

    
    # Adds a queue_item object to self.current_queue
    def add_to_queue(self, url):
        
        print_url = False
        got_from = "url"
        
        if self.is_url(url) == None:
            print("we searching")
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

    # use urllib to get youtubes main page with the search_query set to the requested queue item. Should return a video URL
    def get_url_from_search(self, query):
        url_or_term = query.replace(" ", "+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url_or_term)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        
        return url

    def is_url(self, search_query):
        return re.search("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", search_query)
    
    async def play_next(self):
        self.current_queue.pop(0)
        if len(self.current_queue) == 0:
            self.is_playing = False
            return
        await self.play()

    async def skip(self):
        self.voice_channel.stop()

    async def play(self):
        self.is_playing = True
        print(self.current_queue[0].title)
        ffmpeg_opts = {"executable": "C:/Users/aweso/Desktop/Other/yt-dlp/ffmpeg.exe", "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}
        source = await discord.FFmpegOpusAudio.from_probe(self.current_queue[0].i_url, **ffmpeg_opts)
        self.voice_channel.play(source, after= lambda e:asyncio.run_coroutine_threadsafe(self.play_next(), self.voice_channel.loop))

    async def play_ai(self, message):
        if self.is_playing:
            return
        
        engine = pyttsx3.init()
        
        engine.setProperty('rate', 133) 
        engine.save_to_file(message.content, 'speech.mp3')
        engine.runAndWait()
        
        source = await discord.FFmpegOpusAudio.from_probe('speech.mp3')
        self.voice_channel.play(source, after=lambda e: os.remove('speech.mp3'))


class queue_item:
    def __init__(self, url, title, print_url, got_from, i_url) -> None:
        self.url = url
        self.title = title
        self.print_url = print_url
        self.got_from = got_from
        self.i_url = i_url