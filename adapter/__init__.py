"""
Bot 驱动器
"""
import json


class EventData:
    raw: dict

    def __init__(self, content):
        if isinstance(content, str):
            self.raw = json.loads(content)
        elif isinstance(content, dict):
            self.raw = content
        elif isinstance(content, EventData):
            self.raw = content.raw
        else:
            raise ValueError(f"Unknown EventData Type: {type(content)}")

    @property
    def message(self):
        raise NotImplementedError()


class BotApi:
    async def send_message(self):
        raise NotImplementedError()


class BotAdapter:

    def __init__(self, event_handler):
        self.event_handler = event_handler

    async def handler_event(self, event: EventData):
        return await self.event_handler(self.get_api(), event)

    def get_api(self) -> BotApi:
        raise NotImplementedError()

    async def start_event_loop(self) -> None:
        raise NotImplementedError()
