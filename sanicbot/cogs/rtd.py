import nextcord

from nextcord.ext import commands
from dataclasses import dataclass, field

from sanicbot.core.config import config


@dataclass
class Block(object):
    type: str
    id: str


@dataclass
class Result(object):
    title: str
    blocks: list[Block] = field(default_factory=list)


class RTDCog(commands.Cog):
    API_URL = "https://readthedocs.org/api/v2/search/?format=json&project={project}&q={term}&version={version}"
    DOCS_URL = "https://sanic.readthedocs.io/en/{version}/sanic/api/{title}.html#{id}"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='rtd', description='Search readthedocs.io for a search term', guild_ids=[int(config['SANIC']['guild_id'])])
    async def cmd_rtm(self, 
        interaction: nextcord.Interaction,
        term: str = nextcord.SlashOption(name='term', description='The term to search for', required=True), 
        project: str = nextcord.SlashOption(name='project', description='The project to search within', required=False, default='sanic'), 
        version: str = nextcord.SlashOption(name='version', description='The version to search within', required=False, default='stable')
    ) -> None:

        embed = nextcord.Embed(color=nextcord.Color.from_rgb(255, 13, 104))

        url = self.API_URL.format(project=project, term=term, version=version)
        response = await self.bot.httpclient.get(url)
        response_json = response.json()

        if 'results' not in response_json: 
            embed.color = nextcord.Color.brand_red()
            embed.title = "No results found, sorry."
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        results_aggregate: list[Result] = []
        for result in response_json["results"]:
            blocks: list[Block] = []

            for block in result["blocks"]:
                blocks.append(Block(type=block["type"], id=block["id"]))

            result = Result(title=result["title"], blocks=blocks)
            results_aggregate.append(result)

        added = 0
        for result in results_aggregate:
            if added >= 5: break

            block_data = ""

            for block in result.blocks:
                if added >= 5: break

                if block.type == "domain" and not block.id.startswith("module-"):
                    block_data += f"[{block.id}]"
                    block_data += f"({self.DOCS_URL.format(version='latest', title=result.title.lower(), id=block.id)})\n"
                    added += 1

            if block_data:
                block_data = block_data.rstrip("\n")
                embed.add_field(name=result.title, value=block_data, inline=False)

        await interaction.response.send_message(embed=embed)
