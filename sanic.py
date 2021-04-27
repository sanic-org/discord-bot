from discord.ext import commands

from sanicbot.core.cogs import IssueCog, HelpCog
from sanicbot.core.config import config

bot = commands.Bot(help_command=None, command_prefix=None)

if __name__ == '__main__':
    bot.command_prefix = config['SANIC']['prefix']
    bot.add_cog(IssueCog(bot))
    bot.add_cog(HelpCog(bot))
    bot.run(config['SANIC']['token'], bot=True)