import aiohttp
import nextcord
from nextcord.ext import commands
from ..core import NextityBot
from typing import Callable, Optional

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
        ), ephemeral=True)


def setup(bot: NextityBot) -> None:
    bot.add_cog(BaseCog(bot))
