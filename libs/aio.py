"""
Asyncio
"""
import asyncio
import platform
from functools import partial


def add_task(future):
    asyncio.get_event_loop()


async def run_async(sync_func, *args, **kwargs):
    return await asyncio.get_event_loop().run_in_executor(None, partial(sync_func, *args, **kwargs))


def run_sync(future):
    asyncio.get_event_loop().run_until_complete(future)


def check_windows_event_loop_policy():
    if platform.system() == 'Windows':
        if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def run(future_main):
    check_windows_event_loop_policy()
    asyncio.run(future_main)
