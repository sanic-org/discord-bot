from discord import Embed
from discord.ext.commands import Context


async def failure_message(ctx: Context, message: str):
    await ctx.send(':x: **' + message + '**')


async def success_message(ctx: Context, message: str, embed: Embed = None):
    message = ':white_check_mark: ** ' + message + '**'
    await ctx.send(message, embed=embed)

