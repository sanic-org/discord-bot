import nextcord
import aiohttp
import logging

from nextcord.ext import commands

from sanicbot import cogs
from sanicbot.core import exceptions
from sanicbot.core.config import config
from sanicbot.core import startup


# Register cogs
REGISTERED_COGS = [
    cogs.HelpCog,
    cogs.GitCog
]

if bool(config['SANIC']['debug']):
    logging.basicConfig(level=logging.INFO)

class SanicBot(commands.Bot):
    DEBUG = bool(config['SANIC']['debug'])
    httpclient = None

    def __init__(self, *args, **kwargs):
        intents = nextcord.Intents.all()
        intents.members = True
        super().__init__(*args, command_prefix='!', intents=intents, **kwargs)

    # Server Events
    async def on_connect(self):
        # Limit use to a specific guild
        self.guild = None
        for guild in self.guilds:
            if str(guild.id) == config['SANIC']['guild_id']:
                self.guild = guild
                break
        if not self.guild:
            raise exceptions.InvalidGuild()

        # Register the cogs
        for cog in REGISTERED_COGS:
            self.add_cog(cog(self))
        self.add_all_cog_commands()

        await super().on_connect()

    async def on_ready(self):

        # Setup clients and bindings
        self.httpclient = aiohttp.ClientSession()

        # Initialize the server
        startup.setup_server(self, config)

    async def close(self):
        if self.httpclient:
            await self.httpclient.close()
        await super().close()

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_member_join(self, member):
        pass

    # Helpers
    async def logit(self, message):
        if self.DEBUG:
            await self.debug_channel.send(message)


# Initialize the bot
bot = SanicBot(help_command=None)


# Run the bot
if __name__ == '__main__':
    try:
        bot.run(config['SANIC']['token'])
    except KeyboardInterrupt:  
        asyncio.get_event_loop().run_until_complete(bot.close())

