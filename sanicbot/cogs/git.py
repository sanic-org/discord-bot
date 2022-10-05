import re
import nextcord

from nextcord.ext import commands

from sanicbot.core.config import config
from sanicbot.core.utils import success_message, failure_message


class GitCog(commands.Cog):
    issue_pattern = re.compile(r"#(?P<issue_id>[1,2]\d{3})")

    def __init__(self, bot):
        self.bot = bot

    async def lookup(self, channel: nextcord.TextChannel, number: int, repo: str):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization. Redirection to
        retrieve pull request is automatic due to the fact that Github issues them sequentially.

        :param interaction: Nextcord Interaction.

        :param number: Issue number.

        :param repo: Repository of issue being looked up.

        :return: url, response_code
        """
        url = f"https://github.com/sanic-org/{repo}/issues/{number}"
        async with self.bot.httpclient.get(url) as response:
            if response.status == 200:
                await success_message(channel, f"Issue in {repo} has been found.\n{url}")
            else:
                await failure_message(channel, f"Issue in {repo} has not been found.")
            return str(response.url), response.status

    @nextcord.slash_command(name='issue', description='Lookup an issue', guild_ids=[int(config['SANIC']['guild_id'])])
    async def retrieve_github_issue(self, 
        interaction: nextcord.Interaction, 
        number: int = nextcord.SlashOption(name='number', required=True, description='The issue number to lookup.'), 
        repo: str = nextcord.SlashOption(name='repo', required=False, default='sanic', description='The repo in which to find the issue.')
    ):
        if not repo.startswith("sanic"):
            repo = f"sanic-{repo}"
        await self.lookup(interaction.channel, number, repo)

    @commands.Cog.listener('on_message')
    async def github_issue_message_listener(self, message: nextcord.Message):
        if not message.author.bot:
            if match := self.issue_pattern.search(message.content):
                await self.lookup(
                    message.channel, int(match.group("issue_id")), "sanic"
                )
            else:
                await self.bot.process_commands(message)

