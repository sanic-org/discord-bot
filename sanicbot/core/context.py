import functools
import discord


def user_has_role(discord_user, want_role):
    """
    This helper function requires discord_user to have want_role
    """
    if want_role not in discord_user.roles:
        return False
    return True


def validate_context(want_origins=None, want_roles=None):
    """
    This decorator follows @commands.command() and runs checks and preloading.
        :want_origins: is a list of channel names. requires command to be issued from one of want_origins
        :want_roles: is a list of roles. requires author to be one of want_roles 
    """

    # Allow for a single origin/role to be passed
    if want_origins and not isinstance(want_origins, list): want_origins = [want_origins]
    if want_roles and not isinstance(want_roles, list): want_roles = [want_roles]

    # Build decorator
    def decorator(func):
        """
        This decorator returns an unexecuted wrapped function.
        """

        @functools.wraps(func)
        async def _cmd_wrapper(cog, ctx, *args, **kwargs):
            """
            This inner wrapper is where processing happens.
            """

            # Check did command originates from a DM, and that allow_dm is True
            if isinstance(ctx.channel, discord.channel.DMChannel):
                return

            # Check does ctx.author have one of want_roles (will not work on a DM)
            if want_roles:
                found_role = False
                for role in want_roles:
                    role = discord.utils.get(ctx.guild.roles, name=role)
                    if user_has_role(ctx.author, role):
                        found_role = True
                if not found_role: 
                    await cog.bot.logit(f'!!! **Unauthorized:** {ctx.author.mention} issued command {ctx.message.content}')
                    await ctx.message.delete()
                    return

            # Check did this command originate at at one of want_origins
            if want_origins:
                if ctx.channel.name not in want_origins:
                    await cog.bot.logit(f'{ctx.author.mention} issued {ctx.message.content} from {ctx.channel.mention}. Run this command from {want_origins}')
                    await ctx.message.delete()
                    return

            # run the function
            try:
                return await func(cog, ctx, *args, **kwargs)
            except Exception as err:
                print(err)

        return _cmd_wrapper
    return decorator

