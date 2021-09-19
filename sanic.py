from discord.ext import commands
from discord import Embed
from sanicbot.core.config import config
import aiohttp
from asyncio import run as asynciorun

class embeddedHelpCommand(commands.MinimalHelpCommand):   # help command embedded, subclassed of the minimal help command
    async def send_pages(self):
        destination = self.get_destination()    #get where to send
        with open("./resources/help.txt") as f:
            embed = Embed(description=f.read()) # set desc as page  
        await destination.send(embed=embed) # send embed


async def startup():
    bot = commands.Bot(help_command=embeddedHelpCommand(), command_prefix='!')
    bot.load_extension('sanicbot.core.github')

    async with aiohttp.ClientSession() as session:
        bot.session = session   # set "session" as a botvar so you can access with bot.session anywhere you can touch bot
        await bot.start(config['SANIC']['token'])

if __name__ == '__main__':
    asynciorun(startup())
