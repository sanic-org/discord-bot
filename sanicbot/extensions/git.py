import re

import httpx
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from sanicbot.core.config import config
from sanicbot.core.utils import failure_message, success_message


class Git(commands.Cog):
    issue_pattern = re.compile(r"#(?P<issue_id>[1,2]\d{3})")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def lookup(self, ctx: Context, number: int, repo: str):
        """
        Lookup the issue and check if it exists within a repo found in the Sanic organization. Redirection to
        retrieve pull request is automatic due to the fact that Github issues them sequentially.

        :param ctx: Discord context.

        :param number: Issue number.

        :param repo: Repository of issue being looked up.

        :return: url, response_code
        """
        url = f"https://github.com/sanic-org/{repo}/issues/{number}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                await success_message(ctx, f"Issue in {repo} has been found.\n{url}")
            else:
                await failure_message(ctx, f"Issue in {repo} has not been found.")
            return str(response.url), response.status_code

    @commands.command(aliases=["git", "gh"])
    async def retrieve_github_issue(
        self, ctx: Context, number: int, repo: str = "sanic"
    ):
        if not repo.startswith("sanic"):
            repo = f"sanic-{repo}"
        await self.lookup(ctx, number, repo)

    @commands.command()
    async def issue(self, ctx: Context, repo: str, title: str, *, content: str) -> None:
        repo = repo if not repo.startswith("sanic") else "sanic-" + repo
        url = f"https://api.github.com/repos/sanic-org/{repo}/issues"
        body = f"Forwarded from discord (Author: {ctx.author}, ID: {ctx.author.id})\n" + content
        data = {
            "title": title,
            "body": body,
        }
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + config["SANIC"]["git_token"]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            if response.status_code == 200:
                await success_message(ctx, "Issue created\n" + response.json()["url"])
            else:
                await failure_message(ctx, "An error occured: `" + response.json()["message"] + "`")

    @commands.Cog.listener('on_message')
    async def github_issue_message_listener(self, message: Message):
        if not message.author.bot:
            if match := self.issue_pattern.search(message.content):
                await self.lookup(
                    message.channel, int(match.group("issue_id")), "sanic"
                )


def setup(bot: commands.Bot):
    bot.add_cog(Git(bot))
