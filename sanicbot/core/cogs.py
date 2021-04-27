import aiohttp
from discord.ext import commands
from discord.ext.commands import Context

from sanicbot.core.utils import failure_message, success_message, read_file


class GitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.org_url = f'https://github.com/sanic-org/'

    async def lookup(self, number: int, repo):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization. Redirection to
        retrieve pull request is automatic due to the fact that Github issues them sequentially.

        :param number: Issue number

        :param repo: Repository of issue being looked up

        :return: url, response_code
        """
        url = f'https://github.com/sanic-org/{repo}/issues/{number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return str(response.url), response.status

    @commands.command(aliases=['git', 'g'])
    async def get_issue_or_pull(self, ctx: Context, number: int, repo: str = 'sanic'):
        repo = 'sanic-' + repo if repo != 'sanic' else 'sanic'
        url, lookup_status = await self.lookup(number, repo)
        if lookup_status == 200:
            await success_message(ctx, 'Github issue or pull request in ' + repo + ' found.\n' + url)
        else:
            await failure_message(ctx, 'Github issue or pull request in ' + repo + ' has not been found.')


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(await read_file('help.txt'))
