from dataclasses import dataclass

from adapter import BotApi, BotEvent, BotEventType
from bot import ContextManager

__all__ = [
    "BotApi", "BotEvent", "BotEventType",
    "BotCommand", "BotCommand", "BotCommandOption",
    "name", "description"
]

name = ""
"""模块名称"""

description = ""
"""模块描述"""


@dataclass
class BotCommandOption:
    name: str = None
    """选项名称"""

    alias: list[str] = None
    """选项别名"""

    description: str = ""
    """选项描述"""

    content_type: type = str
    """内容类型"""


class BotCommand:
    name: str = None
    """指令名称"""

    alias: list[str] = None
    """指令别名"""

    description: str = None
    """指令描述"""

    allow_type: list[BotEventType] = None
    """允许使用此指令的消息类型"""

    admin_only: bool = False
    """是否为管理员指令"""

    options: list[BotCommandOption] = None
    """对应的指令选项列表"""

    context: "ContextManager" = None
    """Bot 上下文对象"""

    async def handle(self, bot: BotApi, event: BotEvent) -> bool:
        """
        事件处理函数, 将在每一次触发事件时调用
        :param bot: 事件对应的 bot 端
        :param event: 事件
        :return: 返回 True 表示拦截该消息, 不再继续传给其他模块处理
        """
        raise NotImplementedError()


class BotTask:
    name: str = None
    """任务名称"""

    description: str = None
    """任务描述"""

    cron: str = ""
    """Cron 表达式"""

    context: "ContextManager" = None
    """Bot 上下文对象"""

    async def run(self):
        """任务处理函数, 将在每一个设定的周期执行"""
        raise NotImplementedError()


def bot_command():
    pass


def bot_task():
    pass
