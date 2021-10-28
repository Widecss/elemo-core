"""
Asyncio
"""
import asyncio
import platform
from functools import partial


def add_task_to_event_loop(async_func):
    return asyncio.get_event_loop().create_task(async_func)


async def async_run_until_complete(sync_func, *args, **kwargs):
    return await asyncio.get_event_loop().run_in_executor(None, partial(sync_func, *args, **kwargs))


def sync_run_until_complete(future):
    """用于在事件循环之外同步运行异步函数, 在循环内使用会抛出循环正在运行的异常"""
    return asyncio.get_event_loop().run_until_complete(future)


def check_windows_event_loop_policy():
    if platform.system() == 'Windows':
        if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def run(future_main):
    check_windows_event_loop_policy()
    asyncio.run(future_main)
