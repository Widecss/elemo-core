"""
程序入口
"""
from adapter import BotAdapter, BotEvent
from libs import aio


class ContextManager:
    adapters: list
    modules: list

    def __init__(self):
        self.adapters = []
        self.modules = []

        self.inject_adapters()
        self.inject_modules()

    def inject_adapters(self):
        pass

    def inject_modules(self):
        pass

    async def handler_event(self, bot: BotAdapter, event: BotEvent):
        for module in self.modules:
            await module.handler(bot, event)

    async def _loop(self):
        pass

    def loop(self):
        aio.run(self._loop())


def main():
    context = ContextManager()
    context.loop()


if __name__ == '__main__':
    main()
