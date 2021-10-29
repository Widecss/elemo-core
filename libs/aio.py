"""
Asyncio
"""
import asyncio
import platform
from functools import partial


def create_task_and_start(async_func):
    """创建任务并运行"""
    return asyncio.get_event_loop().create_task(async_func)


async def async_run_until_complete(sync_func, *args, **kwargs):
    """将同步函数运行在异步线程池中"""
    return await asyncio.get_event_loop().run_in_executor(None, partial(sync_func, *args, **kwargs))


def sync_run_until_complete(future):
    """在事件循环之外同步运行异步函数,

    不能在循环内使用, 否则会因为嵌套而抛出循环正在运行的异常"""
    return asyncio.get_event_loop().run_until_complete(future)


def check_windows_event_loop_policy():
    """当运行在 Windows 时, 设置 Windows 的事件循环, 防止各种奇妙问题"""
    if platform.system() == 'Windows':
        if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def run(future_main):
    """运行主协程"""
    check_windows_event_loop_policy()
    asyncio.run(future_main)
