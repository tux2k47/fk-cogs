from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import discord
from datetime import datetime


class CommandLogger(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 123456, True)
        self.config.register_member(commands={})
        # Data structure: commands = {"name":{timestamp:"content"}}

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        async with self.config.member(ctx.author).commands() as commands_dict:
            try:
                commands_dict[ctx.command.qualified_name][
                    datetime.now().timestamp()
                ] = ctx.message.content
            except KeyError:
                name_dict = {datetime.now().timestamp(): ctx.message.content}
                commands_dict[ctx.command.qualified_name] = name_dict

    @commands.is_owner()
    @commands.group()
    async def cmdlog(self, ctx):
        """Commandlog"""
        pass

    @cmdlog.command(name="user")
    async def cmdlog_user(self, ctx, user: discord.Member):
        """Get the command log for a user."""
        data = await self.config.member(user).commands()
        pages = []
        for command in data:
            for timestamp in data[command]:
                e = discord.Embed(
                    title=f"Commandlog for {user.display_name}",
                    description=f"Command: ``{command}``",
                )
                e.add_field(name="Content", value=data[command][timestamp], inline=False)
                e.add_field(
                    name="Timestamp",
                    value=datetime.fromtimestamp(float(timestamp)).strftime(
                        "%H:%M:%S | %d %b %Y UTC"
                    ),
                )
                e.color = discord.Color.dark_blue()
                pages.append(e)
        await menu(ctx, pages, DEFAULT_CONTROLS, timeout=120)

    @cmdlog.command(name="both")
    async def cmdlog_command_and_user(self, ctx, user: discord.Member, *, command: str):
        """Get the command log for a user using a specified command."""
        data = await self.config.member(user).commands()
        pages = []
        for timestamp in data[command]:
            e = discord.Embed(
                title=f"Commandlog for {user.display_name}",
                description=f"Command: ``{command}``",
            )
            e.add_field(name="Content", value=data[command][timestamp], inline=False)
            e.add_field(
                name="Timestamp",
                value=datetime.fromtimestamp(float(timestamp)).strftime("%H:%M:%S | %d %b %Y UTC"),
            )
            e.color = discord.Color.green()
            pages.append(e)
        await menu(ctx, pages, DEFAULT_CONTROLS, timeout=120)

    @cmdlog.command(name="command")
    async def cmdlog_command(self, ctx, *, command: str):
        """Get the command log for a user using a specified command."""
        members = await self.config.all_members(ctx.guild)
        for member in members:
            data = members[member]
            pages = []
            try:
                for timestamp in data[command]:
                    user = ctx.guild.get_member(member)
                    e = discord.Embed(
                        title=f"Commandlog for ``{command}``",
                        description=f"Invoked by: {user.mention}({user.name}#{user.discriminator} {user.id}",
                    )
                    e.add_field(name="Content", value=data[command][timestamp], inline=False)
                    e.add_field(
                        name="Timestamp",
                        value=datetime.fromtimestamp(float(timestamp)).strftime(
                            "%H:%M:%S | %d %b %Y UTC"
                        ),
                    )
                    e.color = discord.Color.orange()
                    pages.append(e)
            except KeyError:
                pass
        try:
            await menu(ctx, pages, DEFAULT_CONTROLS, timeout=120)
        except IndexError:
            await ctx.send("Command not tracked yet.")