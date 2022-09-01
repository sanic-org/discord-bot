import discord

def setup_server(bot, config):
    # Setup channels
    bot.debug_channel = discord.utils.get(bot.guild.channels, name=config['SANIC']['debug_channel_name'])

    # Setup roles
    bot.voting_role = discord.utils.get(bot.guild.roles, name=config['SANIC']['voting_role_name'])