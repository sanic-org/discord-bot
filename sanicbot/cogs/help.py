import nextcord

from nextcord.ext import commands

from sanicbot.core.config import config


class HelpCog(commands.Cog):
    @nextcord.slash_command(name='commands', description='List available commands', guild_ids=[int(config['SANIC']['guild_id'])])
    async def cmd_help(self, interaction: nextcord.Interaction):
        with open("./resources/help.txt") as f:
            await interaction.response.send_message(f.read())
        return

