import discord
import aiohttp

from discord.ext import commands

from sanicbot.core import cogs
from sanicbot.core import exceptions
from sanicbot.core.config import config
from sanicbot.core.startup import startup

# Register cogs
REGISTERED_COGS = [
    cogs.HelpCog,
    cogs.GitCog
]


class SanicBot(commands.Bot):
    DEBUG = config['SANIC']['debug']

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(*args, command_prefix='!', intents=intents, **kwargs)

        self.httpclient = aiohttp.ClientSession()

        for cog in REGISTERED_COGS:
            self.add_cog(cog(self))

    # Server Events
    async def on_ready(self):
        # Set the guild (limit the bot usage to a given guild_id)
        self.guild = None
        for guild in self.guilds:
            if guild.id == config['SANIC']['guild_id']
                self.guild = guild
                break
        if not self.guild:
            raise exceptions.InvalidGuild()

        # Initialize the server
        startup.setup_server(self, config)

    async def on_message(self, message):
        await self.process_commands(message)

    async def close(self):
        await self.httpclient.close()
        await super().close()

    async def on_member_join(self, member):
        pass

    # Helpers
    async def logit(self, message):
        if self.DEBUG:
            await self.debug_channel.send(message)
        print(message)


# Initialize the bot
bot = SanicBot(help_command=None)


# Run the bot
if __name__ == '__main__':
    try:
        bot.run(config['SANIC']['token'])
    except KeyboardInterrupt:    
        pass