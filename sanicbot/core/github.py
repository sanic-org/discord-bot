import re

from aiohttp import ClientSession
from discord import Message
from discord.ext import commands
from sanicbot.core.utils import failure_message, success_message


class GitCog(commands.Cog):
    issue_pattern = re.compile(r"#(?P<issue_id>[1,2]\d{3})")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()    # no where else to throw this so lets put it here
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    async def lookup(self, ctx: commands.Context, number: int, repo: str):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization. Redirection to
        retrieve pull request is automatic due to the fact that Github issues them sequentially.

        :param number: Issue number.

        :param repo: Repository of issue being looked up.

        :return: url, response_code
        """
        url = f"https://github.com/sanic-org/{repo}/issues/{number}"
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                await success_message(ctx, f"Issue in {repo} has been found.\n<{url}>")
            else:
                await failure_message(ctx, f"Issue in {repo} has not been found.")

    @commands.command(aliases=["git", "gh"])
    async def retrieve_github_issue(self, ctx: commands.Context, number: int, repo: str = "sanic"):
        await ctx.trigger_typing()
        if not repo.startswith("sanic"):
            repo = f"sanic-{repo}"
        await self.lookup(ctx, number, repo)
    
    @commands.Cog.listener(name='on_message')
    async def github_issue_message_listener(self, message: Message):
        if not message.author.bot:
            if match := self.issue_pattern.search(message.content):
                await self.lookup(message.channel, int(match.group("issue_id")), "sanic")

def setup(bot):
    bot.add_cog(GitCog(bot))
