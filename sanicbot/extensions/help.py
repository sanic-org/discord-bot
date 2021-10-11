from discord.ext import commands


class Help(commands.Cog):
    @commands.command()
    async def help(self, ctx):
        with open("./resources/help.txt") as f:
            await ctx.send(f.read())


def setup(bot: commands.Bot):
    bot.add_cog(Help())
    