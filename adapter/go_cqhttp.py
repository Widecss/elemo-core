"""
Go_CQHttp 适配器
"""
import logging

from aiohttp import (
    WSMsgType,
    ClientSession,
    WSMessage
)

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
        return text.content

    def dump_image(self, image: Image):
        _ctn = self._escape_cq_code(image.content)
        return f"[CQ:image,file={_ctn}]"

    def dump_audio(self, audio: Audio):
        _ctn = self._escape_cq_code(audio.content)
        return f"[CQ:record,file={_ctn}]"

    @staticmethod
    def _escape_cq_code(text: str):
        return text.replace(",", "&#44;") \
            .replace("&", "&amp;") \
            .replace("[", "&#91;") \
            .replace("]", "&#93;")


class GoCQHttpAdapter(BotAdapter):

    async def create_api(self) -> BotApi:
        return GoCQHttpApi()

    async def create_parser(self) -> GoCQHttpEventParser:
        return GoCQHttpEventParser()

    async def data_receiver(self, response: WSMessage):
        if response.type == WSMsgType.TEXT:
            await self.handle_event(response.json())
        elif response.type == WSMsgType.ERROR:
            logging.error(f"GoCQHttp receive error: {response.data}")

    async def on_start(self) -> None:
        async with ClientSession() as session:
            async with session.ws_connect('http://127.0.0.1:6700/event') as ws:
                response: WSMessage
                async for response in ws:
                    await self.data_receiver(response)
