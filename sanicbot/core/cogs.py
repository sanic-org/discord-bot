import aiohttp
from discord.ext import commands
from discord.ext.commands import Context

from sanicbot.core.utils import failure_message, success_message


class IssueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def issue_lookup(self, number: int, repo: str, ):
        url = f'https://github.com/sanic-org/{repo}/issues/{number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return url, response.status

    @commands.command(aliases=['issue', 'i'])
    def get_issue(self, ctx: Context, number: int, repo: str = 'sanic'):
        url, lookup_status = self.issue_lookup(number, repo)
        if lookup_status == 200:
            await success_message(ctx, url)
        else:
            await failure_message(ctx, 'Issue retrevial failed with error code:' + str(lookup_status))


