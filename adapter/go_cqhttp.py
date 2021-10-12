import logging

from aiohttp import WSMsgType

from tools.message_chain import MessageChain, Image, Text
from . import (
    BotAdapter,
    BotApi,
    BotEvent,
    MessageParser
)


class GoCQHttpMessageParser(MessageParser):

    def _dump_text(self, text: Text):
        return text

    def _dump_image(self, image: Image):
        pass


class GoCQHttpEvent(BotEvent):
    @property
    def message(self):
        return


class GoCQHttpApi(BotApi):
    async def reply(self, message_chain: MessageChain):
        pass


class GoCQHttpAdapter(BotAdapter):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.api = GoCQHttpApi()

    def get_api(self) -> BotApi:
        return self.api

    async def data_receiver(self, session):
        async with session.ws_connect('http://127.0.0.1:6700/') as ws:
            async for response in ws:
                if response.type == WSMsgType.TEXT:
                    await self.handler_event(response.data)
                elif response.type == WSMsgType.ERROR:
                    logging.error(f"GoCQHttp receive error: {response.data}")

    async def start_event_loop(self) -> None:
        pass
        # async with aiohttp.ClientSession() as session:
        #     await ws_handler(session)
