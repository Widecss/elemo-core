"""
Bot 驱动器
"""
from enum import Enum

from tools.message_chain import (
    MessageNode,
    MessageChain,
    Text, Image, Audio
)

__all__ = ["BotAdapter", "BotEventType", "BotEvent", "BotApi", "BotEventParser"]


class BotEventType(Enum):
    """Bot 事件类型"""

    NoticeMessage = "NoticeMessage"
    """提示消息"""

    RequestMessage = "RequestMessage"
    """请求消息"""

    GroupCommand = "GroupCommand"
    """群组指令"""

    FriendCommand = "FriendCommand"
    """私人指令"""

    GroupMessage = "GroupMessage"
    """群组消息"""

    FriendMessage = "FriendMessage"
    """私人消息"""


class BotEvent:
    """Bot 事件"""
    @property
    def event_type(self) -> BotEventType:
        """事件类型"""
        raise NotImplementedError()

    @property
    def sender_id(self) -> str:
        """发送者 id"""
        raise NotImplementedError()

    @property
    def sender_name(self) -> str:
        """发送者名称"""
        raise NotImplementedError()

    @property
    def group_id(self) -> str:
        """群组 id, 在非群组消息时可能为空"""
        raise NotImplementedError()

    @property
    def group_name(self) -> str:
        """群组名称, 在非群组消息时可能为空"""
        raise NotImplementedError()

    @property
    def message(self) -> MessageChain:
        """消息内容"""
        raise NotImplementedError()

    @property
    def command(self) -> str:
        """触发的指令"""
        raise NotImplementedError()

    @property
    def command_options(self) -> list[tuple[str, str]]:
        """触发的指令对应的选项

        格式为 [("name", "content"), ...]"""
        raise NotImplementedError()

    @property
    def command_argv(self) -> str:
        """触发的指令对应的参数, 也就是后方对应的无选项内容

        格式为 [("name", "content"), ...]"""
        raise NotImplementedError()


class BotEventParser:
    def dump(self, message_node: MessageNode):
        """将消息链的节点转换成原始数据

        :param message_node: 消息链的节点
        :return: 原始数据
        """
        for _type, _func in [
            (Text, self.dump_text),
            (Image, self.dump_image),
            (Audio, self.dump_audio)
        ]:
            if isinstance(message_node, _type):
                return _func(message_node)
        return None

    def load(self, event_data) -> BotEvent:
        raise NotImplementedError()

    def dump_text(self, text: Text):
        """将文本消息节点转换成原始数据

        :param text: 文本消息
        :return: 原始数据
        """
        raise NotImplementedError()

    def dump_image(self, image: Image):
        """将图片消息节点转换成原始数据

        :param image: 图片消息
        :return: 原始数据
        """
        raise NotImplementedError()

    def dump_audio(self, audio: Audio):
        """将音频消息节点转换成原始数据

        :param audio: 音频消息
        :return: 原始数据
        """
        raise NotImplementedError()


class BotApi:
    async def reply(self, message_chain: MessageChain):
        raise NotImplementedError()


class BotAdapter:
    """Bot客户端的适配器

    使用 start_event_loop() 异步开启循环

    使用 handler_event() 传入自定义 BotEvent 以处理事件
    """
    event_handler = None
    """事件处理器, 在适配器加载时注入"""

    async def handle_event(self, event_data):
        """将事件传入以进行处理

        :param event_data: 事件数据, 将直接传给 BotEventParser.load()
        """
        if self.event_handler:
            await self.event_handler(
                self.get_api(),
                self.get_parser().load(event_data)
            )

    def get_api(self) -> BotApi:
        """将自定义的 BotApi 传出

        :return: 自定义的 BotApi
        """
        raise NotImplementedError()

    def get_parser(self) -> BotEventParser:
        """将自定义的 BotEventParser 传出

        :return: 自定义的 BotEventParser
        """
        raise NotImplementedError()

    async def start(self):
        """启动时"""
        raise NotImplementedError()

    async def close(self):
        """关闭时"""
        raise NotImplementedError()
