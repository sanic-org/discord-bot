import nextcord
import httpx
import logging

from nextcord.ext import commands

from sanicbot import cogs
from sanicbot.core import exceptions
from sanicbot.core.config import config


# Register cogs
REGISTERED_COGS = [
    cogs.GitCog,
    cogs.RTDCog
]

# Set root log level
logging.basicConfig(level=logging.INFO)

class SanicBot(commands.Bot):
    DEBUG = config['SANIC'].getboolean('debug', False)
    httpclient = None

    def __init__(self, *args, **kwargs):
        intents = nextcord.Intents.all()
        intents.members = True

        self.logger = logging.getLogger(config['SANIC']['BOT_NAME'])
        self.logger.setLevel(logging.DEBUG if self.DEBUG else logging.INFO)

        super().__init__(*args, command_prefix='!', intents=intents, **kwargs)

    # Server Events
    async def on_connect(self) -> None:
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

    async def on_ready(self) -> None:

        # Setup clients and bindings
        self.httpclient = httpx.AsyncClient()

        # Initialize the server
        
        self.logger.debug('Starting in DEBUG mode.')

    async def close(self) -> None:
        if self.httpclient:
            await self.httpclient.aclose()
        await super().close()

    async def on_message(self, message: nextcord.Message) -> None:
        await self.process_commands(message)

    async def on_member_join(self, member: nextcord.Member) -> None:
        pass


# Initialize the bot
bot = SanicBot(help_command=None)


# Run the bot
if __name__ == '__main__':
    try:
        bot.run(config['SANIC']['token'])
    except KeyboardInterrupt:  
        asyncio.get_event_loop().run_until_complete(bot.close())

