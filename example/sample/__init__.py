"""
简单的例子
"""
from module import *

name = "演示"
description = "一个演示用的模块"


class Echo(BotCommand):
    def __init__(self):
        self.name = "echo"
        self.description = "回显指令"

        self.allow_type = [BotEventType.FriendCommand]
        self.admin_only = True

        self.options = [
            BotCommandOption(
                name="escape",
                alias=["e"],
                description="是否转义输入的文字",
                content_type=bool
            )
        ]

    async def handle(self, bot: BotApi, event: BotEvent) -> bool:
        pass
