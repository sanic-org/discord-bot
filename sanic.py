from discord import Message
from discord.ext import commands

from sanicbot.core.cogs import HelpCog, GitCog
from sanicbot.core.config import config

bot = commands.Bot(help_command=None, command_prefix=None)
git_cog = GitCog(bot)


@bot.event
async def on_message(message):
    await github_issue_listener(message)


async def github_issue_listener(message: Message):
    if not message.author.bot:
        if match := git_cog.issue_pattern.search(message.content):
            await git_cog.lookup(message.channel, match.group("issue_id"), 'sanic')
        else:
            await bot.process_commands(message)


if __name__ == '__main__':
    bot.command_prefix = '!'
    bot.add_cog(git_cog)
    bot.add_cog(HelpCog(bot))
    bot.run(config['SANIC']['token'], bot=True)
