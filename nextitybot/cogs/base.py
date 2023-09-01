import aiohttp
import nextcord
from nextcord.ext import commands
from ..core import NextityBot
from typing import Callable, Optional


class BotinfoView(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=0.0)
        self.add_item(nextcord.ui.Button(
            style=nextcord.ButtonStyle.link,
            url="https://github.com/DarpHome/nextitybot",
            emoji="<:dh_github_octocat:1147138555202773062>",
        ))


class BaseCog(commands.Cog):
    bot: NextityBot
    def __init__(self, bot: NextityBot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="ping",
        description="Ping",
        dm_permission=True,
    )
    async def ping(self, inter: nextcord.Interaction) -> None:
        await inter.response.send_message(f"🏓 Latency: {self.bot.latency:.3f}", ephemeral=True)

    @nextcord.slash_command(
        name="bot",
        description="Bot",
        dm_permission=True,
    )
    async def bot(
        self,
        inter: nextcord.Interaction,
    ) -> None:
        await inter.response.send_message(embed=nextcord.Embed(
            title="Me",
        ).add_field(
            name="Support server",
            value="[Click](https://discord.gg/EVtSwKttEH)",
        ).set_author(
            name=inter.user.name,
            icon_url=inter.user.display_avatar.url,
        ).set_footer(
            text="NextityBot",
            icon_url=self.bot.user.display_avatar.url,
        ), view=BotinfoView(), ephemeral=True)


def setup(bot: NextityBot) -> None:
    bot.add_cog(BaseCog(bot))
