import aiohttp
import nextcord
from nextcord.ext import commands, tasks
import itertools
import logging
import time
from typing import Optional

logging.basicConfig(level=logging.INFO)

Presence = tuple[Optional[nextcord.BaseActivity], Optional[nextcord.Status]]

async def presence_show_information(bot: "NextityBot") -> Presence:
    bot.updated_count += 1
    return (
        nextcord.Activity(
            name=f"{bot.updated_count} | {len(bot.users)} users | {len(bot.guilds)} servers",
            type=nextcord.ActivityType.listening,
        ),
        nextcord.Status.online,
    )

class NextityBot(commands.AutoShardedBot):
    presences_iterator: itertools.cycle # cannot be annotated at 26.08.2023
    updated_count: int
    logger: logging.Logger
    def __init__(self) -> None:
        super().__init__(intents=nextcord.Intents.all())
        self.presences_iterator = itertools.cycle([
            presence_show_information,
        ])
        self.updated_count = 0
        self.logger = logging.getLogger('nextitybot.core')

    @tasks.loop(minutes=1.0)
    async def presence_updater(self) -> None:
        presence: Presence = await next(self.presences_iterator)(self)
        await self.change_presence(
            activity=presence[0],
            status=presence[1],
        )

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        self.add_all_application_commands()
        await self.sync_application_commands()
        self.presence_updater.start()

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        self.presence_updater.cancel()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info(f"Logged as {self.user.name}#{self.user.discriminator}!")
