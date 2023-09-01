import dotenv
dotenv.load_dotenv()

import aiohttp
import asyncio
import nextcord
from nextitybot import NextityBot, search_directory
import logging
import os
import sys
import traceback
from typing import Callable

bot: NextityBot = NextityBot()

async def amain() -> None:
    try:
        await bot.login(os.getenv("DISCORD_BOT_TOKEN"))
        bot.load_extensions(search_directory("nextitybot/cogs"))
        await bot.connect()
    except Exception as exception:
        traceback.print_exception(exception)

async def aexit() -> None:
    pass

async def ahandle_exception(raiser: Callable[[], None]) -> None:
    try:
        raiser() # always raises
    except KeyboardInterrupt:
        await aexit()
    except Exception as exception:
        traceback.print_exception(exception)
    else:
        print("something went wrong!!! bot developer go fix!!!!!")

def make_raiser(exception: Exception) -> None:
    def raiser() -> None:
        raise exception
    return raiser

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(amain())
    except Exception as exception:
        loop.run_until_complete(ahandle_exception(make_raiser(exception)))
    finally:
        loop.close()
