from discord.message import Message
from router import router

@router.command('!version')
async def version(var, message: Message):
    with open('./version') as readfile:
        await message.channel.send(readfile.read())