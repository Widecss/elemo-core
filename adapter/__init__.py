"""
Bot 驱动器
"""
from enum import Enum

from tools.message_chain import (
    MessageNode,
    MessageChain,
    Text, Image, Audio
)

__all__ = ["BotAdapter", "EventType", "BotEvent", "BotApi", "MessageParser"]


class MessageParser:
    def dump(self, message_node: MessageNode):
        for _type, _func in [
            (Text, self.dump_text),
            (Image, self.dump_image),
            (Audio, self.dump_audio)
        ]:
            if isinstance(message_node, _type):
                return _func(message_node)
        return None

    def dump_text(self, text: Text):
        raise NotImplementedError()

    def dump_image(self, image: Image):
        raise NotImplementedError()

    def dump_audio(self, audio: Audio):
        raise NotImplementedError()


class EventType(Enum):
    NoticeMessage = "NoticeMessage"
    """提示消息"""

    RequestMessage = "RequestMessage"
    """请求消息"""

    GroupMessage = "GroupMessage"
    """群组消息"""

    FriendMessage = "FriendMessage"
    """私人消息"""


class BotEvent:
    @property
    def event_type(self) -> EventType:
        raise NotImplementedError()

    @property
    def sender_id(self) -> str:
        raise NotImplementedError()

    @property
    def sender_name(self) -> str:
        raise NotImplementedError()

    @property
    def group_id(self) -> str:
        raise NotImplementedError()

    @property
    def group_name(self) -> str:
        raise NotImplementedError()

    @property
    def message(self) -> MessageChain:
        raise NotImplementedError()


class BotApi:
    async def display_setting(self, notice: str, settings: list):
        raise NotImplementedError()

    async def update_setting(self, notice: str, settings: list):
        raise NotImplementedError()

    async def reply(self, message_chain: MessageChain):
        raise NotImplementedError()


class BotAdapter:
    def __init__(self, event_handler):
        self.event_handler = event_handler

    async def handler_event(self, event: BotEvent):
        return await self.event_handler(self.get_api(), event)

    def get_api(self) -> BotApi:
        raise NotImplementedError()

    def get_message_parser(self) -> MessageParser:
        raise NotImplementedError()

    async def start_event_loop(self) -> None:
        raise NotImplementedError()
