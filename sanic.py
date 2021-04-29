from discord.ext import commands

from sanicbot.core.cogs import HelpCog, GitCog
from sanicbot.core.config import config

bot = commands.Bot(help_command=None, command_prefix=None)
git_cog = GitCog(bot)


@bot.event
async def on_message(message):
    await git_cog.github_issue_message_listener(message)


if __name__ == '__main__':
    bot.command_prefix = '!'
    bot.add_cog(git_cog)
    bot.add_cog(HelpCog(bot))
    bot.run(config['SANIC']['token'], bot=True)
