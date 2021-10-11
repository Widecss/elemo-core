"""
Asyncio
"""
import asyncio
import platform
from functools import partial


def add_task(async_func):
    asyncio.get_event_loop().create_task(async_func())


async def async_run_until_complete(sync_func, *args, **kwargs):
    return await asyncio.get_event_loop().run_in_executor(None, partial(sync_func, *args, **kwargs))


def sync_run_until_complete(future):
    asyncio.get_event_loop().run_until_complete(future)


def run_func_until_complete(_func, *args, **kwargs):
    if asyncio.iscoroutinefunction(_func):
        return await _func(*args, **kwargs)
    else:
        return _func(*args, **kwargs)


def check_windows_event_loop_policy():
    if platform.system() == 'Windows':
        if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def run(future_main):
    check_windows_event_loop_policy()
    asyncio.run(future_main)
