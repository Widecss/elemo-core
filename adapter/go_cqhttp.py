"""
Go_CQHttp 适配器
"""
import logging

from aiohttp import WSMsgType, ClientSession, WSMessage

from tools.chain import (
    MessageChain,
    Image, Text, Audio
)
from . import (
    BotAdapter,
    BotApi,
    BotEvent,
    BotEventParser,
    BotEventType
)


class GoCQHttpEvent(BotEvent):
    def __init__(self, raw):
        self.raw = raw

    @property
    def event_type(self) -> BotEventType:
        pass

    @property
    def sender_id(self) -> str:
        pass

    @property
    def sender_name(self) -> str:
        pass

    @property
    def group_id(self) -> str:
        pass

    @property
    def group_name(self) -> str:
        pass

    @property
    def command(self) -> str:
        pass

    @property
    def command_options(self) -> list[tuple[str, str]]:
        pass

    @property
    def command_argv(self) -> str:
        pass

    @property
    def message(self) -> MessageChain:
        pass


class GoCQHttpApi(BotApi):
    async def reply(self, message_chain: MessageChain):
        pass


class GoCQHttpEventParser(BotEventParser):
    def load(self, event_data) -> BotEvent:
        return GoCQHttpEvent(event_data)

    def dump_text(self, text: Text):
        pass

    def dump_image(self, image: Image):
        pass

    def dump_audio(self, audio: Audio):
        pass


class GoCQHttpAdapter(BotAdapter):

    def get_api(self) -> BotApi:
        return GoCQHttpApi()

    def get_parser(self) -> GoCQHttpEventParser:
        return GoCQHttpEventParser()

    async def data_receiver(self, session: ClientSession):
        async with session.ws_connect('http://127.0.0.1:6700/') as ws:
            async for response in ws:
                response: WSMessage
                if response.type == WSMsgType.TEXT:
                    await self.handle_event(response.json())
                elif response.type == WSMsgType.ERROR:
                    logging.error(f"GoCQHttp receive error: {response.data}")

                if ws.closed:
                    break

    async def start(self) -> None:
        async with ClientSession() as session:
            await self.data_receiver(session)

    async def close(self):
        pass
