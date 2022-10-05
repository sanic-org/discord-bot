import nextcord


async def failure_message(channel: nextcord.TextChannel, message: str):
    await channel.send(f":x: **{message}**")


async def success_message(channel: nextcord.TextChannel, message: str, embed: nextcord.Embed = None):
    message = f":white_check_mark: **{message}**"
    await channel.send(message, embed=embed)
