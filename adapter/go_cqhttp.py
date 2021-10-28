"""
Go_CQHttp 适配器
"""
import logging

from aiohttp import (
    WSMsgType,
    ClientSession,
    WSMessage, ClientWebSocketResponse
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


class GoCQHttpEventType(BotEventType):
    GoCQHttpLifecycle = "GoCQHttpLifecycle"
    """生命周期消息"""

    GoCQHttpHeartbeat = "GoCQHttpHeartbeat"
    """心跳消息"""


meta_event_type_str = {
    "lifecycle": GoCQHttpEventType.GoCQHttpLifecycle,
    "heartbeat": GoCQHttpEventType.GoCQHttpHeartbeat
}

message_type_str = {
    "private": GoCQHttpEventType.BotFriendMessage,
    "group": GoCQHttpEventType.BotGroupMessage
}


class GoCQHttpEvent(BotEvent):

    def __init__(self, raw: dict):
        self.raw: dict = raw

    @property
    def timestamp(self) -> int:
        return self.raw["time"]

    @property
    def type(self) -> GoCQHttpEventType:
        post_type = self.raw["post_type"]

        if post_type == "meta_event":
            meta_event_type = self.raw["meta_event_type"]
            if meta_event_type in meta_event_type_str.keys():
                return meta_event_type_str[meta_event_type]

        if post_type == "message":
            message_type = self.raw["message_type"]
            if message_type in message_type_str.keys():
                return message_type_str[message_type]

        return GoCQHttpEventType.BotUnknownTypeMessage

    @property
    def sender_original_id(self) -> str:
        return str(self.raw["user_id"])

    @property
    def sender_name(self) -> str:
        sender: dict = self.raw["sender"]
        if sender["card"]:
            return sender["card"]
        else:
            return sender["nickname"]

    @property
    def group_original_id(self) -> str:
        return str(self.raw["group_id"])

    @property
    def group_name(self) -> str:
        raise KeyError("键名 group_name 不存在")

    @property
    def command(self) -> str:
        raise NotImplementedError()

    @property
    def command_options(self) -> list[tuple[str, str]]:
        raise NotImplementedError()

    @property
    def command_argv(self) -> str:
        raise NotImplementedError()

    @property
    def message(self) -> MessageChain:
        raise NotImplementedError()


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
    ws: ClientWebSocketResponse

    async def create_api(self) -> GoCQHttpApi:
        return GoCQHttpApi()

    async def create_parser(self) -> GoCQHttpEventParser:
        return GoCQHttpEventParser()

    async def data_receiver(self, response: WSMessage):
        if response.type == WSMsgType.TEXT:
            event = response.json()
            await self.handle_event(event)
        elif response.type == WSMsgType.ERROR:
            logging.error(f"GoCQHttp receive error: {response.data}")

    async def on_event_loop(self) -> None:
        async with ClientSession() as session:
            async with session.ws_connect('http://127.0.0.1:6700/event') as ws:
                self.ws = ws
                response: WSMessage
                async for response in ws:
                    await self.data_receiver(response)

    async def on_close(self):
        await self.ws.close()
