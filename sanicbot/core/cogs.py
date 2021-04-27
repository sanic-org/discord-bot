import aiohttp
from discord.ext import commands
from discord.ext.commands import Context

from sanicbot.core.utils import failure_message, success_message, read_file


class GitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.org_url = f'https://github.com/sanic-org/'

    async def lookup(self, number: int, repo: str, git_type: str):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization.

        :param git_type: The type of github link being looked up. Can be issue or pull.

        :param number: Issue number

        :param repo: Repository of issue being looked up

        :return: url, response_code
        """
        url = f'https://github.com/sanic-org/{repo}/{git_type}/{number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return url, response.status

    @commands.command(aliases=['issue', 'i'])
    async def get_issue(self, ctx: Context, number: int, repo: str = None):
        url, lookup_status = await self.lookup(number, repo, 'issue')
        if lookup_status == 200:
            await success_message(ctx, 'Issue in ' + repo + ' found.\n' + url)
        else:
            await failure_message(ctx, 'Issue retrieval failed with error code: ' + str(lookup_status))

    @commands.command(aliases=['pull', 'p'])
    async def get_pull(self, ctx: Context, number: int, repo: str = None):
        url, lookup_status = await self.lookup(number, repo, 'pull')
        if lookup_status == 200:
            await success_message(ctx, 'Pull request in ' + repo + ' found.\n' + url)
        else:
            await failure_message(ctx, 'Pull request retrieval failed with error code: ' + str(lookup_status))


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(await read_file('help.txt'))
