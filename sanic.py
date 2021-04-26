from discord.ext import commands

from sanicbot.core.config import config

bot = commands.Bot(help_command=None, command_prefix=None)

if __name__ == '__main__':
    bot.command_prefix = config['SANIC']['prefix']
    bot.run(config['SANIC']['token'], bot=True)