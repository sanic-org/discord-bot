from discord.ext import commands

from sanicbot.core.config import config


EXTENSIONS = (
    'sanicbot.extensions.git',
    'sanicbot.extensions.help',
)


def main():
    bot = commands.Bot(help_command=None, command_prefix='!')

    for ext in EXTENSIONS:
        bot.load_extension(ext)

    bot.run(config['SANIC']['token'])


if __name__ == '__main__':
    main()
