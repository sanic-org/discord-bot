import httpx
from discord.ext import commands
from discord.ext.commands import Context

from sanicbot.core.utils import failure_message, success_message


class GitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.org_url = f'https://github.com/sanic-org/'

    async def lookup(self, number: int, repo: str):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization. Redirection to
        retrieve pull request is automatic due to the fact that Github issues them sequentially.

        :param number: Issue number

        :param repo: Repository of issue being looked up.

        :return: url, response_code.
        """
        url = f'https://github.com/sanic-org/{repo}/issues/{number}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return str(response.url), response.status

    @commands.command(aliases=['git', 'gh'])
    async def retrieve_issue(self, ctx: Context, number: int, repo: str = 'sanic'):
        if not repo.startswith("sanic"):
            repo = f"sanic-{repo}"
        url, lookup_status = await self.lookup(number, repo)
        if lookup_status == 200:
            await success_message(ctx, f'Github issue or pull request in {repo} found.\n{url}')
        else:
            await failure_message(ctx, f'Github issue or pull request in {repo} has not been found.')


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        await ctx.send()
