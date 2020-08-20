from redbot.core import commands
import discord


def is_amy():
    async def predicate(ctx):
        return ctx.author.id == 716270669725171754

    return commands.check(predicate)


class FakeCTX(discord.Member):
    def __init__(self, author):
        self.author = author


class RaceMock(commands.Cog):
    @is_amy()
    @commands.command()
    async def racemock(self, ctx, member: discord.Member):
        """Allow amy to force people to race"""

        race = bot.get_cog("Race")
        if race.active:
            race.players.append(member)
            await ctx.send(f"Amy forced {member.mention} to race.")
        else:
            await ctx.send(f"There is no race ongoing. Start one first.")