"""
程序入口
"""
from adapter import BotEvent, BotApi, BotAdapter
from libs import aio
from module import BotCommand


class ContextManager:
    __slots__ = ["_adapters", "_commands"]

    def __init__(self):
        self._adapters: list[BotAdapter] = []
        self._commands: list[BotCommand] = []

    async def _inject_adapters(self) -> bool:
        raise NotImplementedError()

    async def _inject_modules(self) -> bool:
        raise NotImplementedError()

    async def reload_module(self, name: str) -> bool:
        raise NotImplementedError()

    async def reload_adapter(self, name: str) -> bool:
        raise NotImplementedError()

    @property
    def adapter_name_list(self) -> list[str]:
        raise NotImplementedError()

    @property
    def command_name_list(self) -> list[str]:
        raise NotImplementedError()

    async def handler_event(self, bot: BotApi, event: BotEvent):
        for _mod in self._commands:
            intercept = await _mod.handle(bot, event)
            if intercept:
                break

    async def _loop(self):
        await self._inject_adapters()
        await self._inject_modules()

    def loop(self):
        aio.run(self._loop())


def main():
    context = ContextManager()
    context.loop()


if __name__ == '__main__':
    main()
