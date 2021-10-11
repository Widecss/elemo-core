from adapter import BotAdapter, EventData


class BotModule:
    async def handler(self, bot: BotAdapter, event: EventData):
        raise NotImplementedError()
