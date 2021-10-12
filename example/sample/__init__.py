"""
简单的例子
"""
from adapter import BotAdapter, BotEvent
from module import BotModule


class Sample(BotModule):
    async def handler(self, bot: BotAdapter, event: BotEvent):
        pass
