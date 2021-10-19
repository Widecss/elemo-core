"""
Bot 驱动器
"""
import builtins
import inspect
import types
from enum import Enum

from libs import dicts
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
        """原消息内容"""
        raise NotImplementedError()

    @property
    def command(self) -> str:
        """触发的指令, 在非指令消息时可能为空"""
        raise NotImplementedError()

    @property
    def command_options(self) -> list[tuple[str, str]]:
        """触发的指令对应的选项, 在非指令消息时可能为空

        格式为 [("name", "content"), ...]"""
        raise NotImplementedError()

    @property
    def command_argv(self) -> str:
        """指令后方的无选项内容, 在非指令消息时可能为空"""
        raise NotImplementedError()


class BotEventParser:
    def dump(self, message_node: MessageNode):
        """将 MessageNode 转换成原始数据

        :param message_node: MessageNode 对象
        :return: 原始数据
        """
        node_name = message_node.__class__.__name__
        func_name = f"dump_{node_name.lower()}"

        self_dict = dicts.filter_mapping(
            lambda key: inspect.isfunction(self_dict[key]),
            self.__class__.__dict__
        )

        if func_name in self_dict.keys():
            return self_dict[func_name](self, message_node)
        return None

    def load(self, event_data) -> BotEvent:
        """将原始事件数据转换成自定义 BotEvent 对象

        :param event_data: 传入 BotAdapter.handle_event() 的事件数据
        :return: 自定义 BotEvent 对象
        """
        raise NotImplementedError()

    def dump_text(self, text: Text):
        """将 Text 节点转换成原始数据

        :param text: Text 节点
        :return: 原始数据
        """
        raise NotImplementedError()

    def dump_image(self, image: Image):
        """将 Image 节点转换成原始数据

        :param image: Image 节点
        :return: 原始数据
        """
        raise NotImplementedError()

    def dump_audio(self, audio: Audio):
        """将 Audio 节点转换成原始数据

        :param audio: Audio 节点
        :return: 原始数据
        """
        raise NotImplementedError()


class BotApi:
    async def reply(self, message_chain: MessageChain):
        raise NotImplementedError()


class BotAdapter:
    """Bot客户端的适配器

    start() 将在启动时调用, 用于开启事件接收
    close() 将在关闭时调用, 用于关闭事件接收

    handle_event() 传入事件数据以处理事件
    """
    event_handler: types.FunctionType = None
    """事件处理器"""

    config: dict = None
    """一些配置"""

    def __init__(self, config=None, event_handler=None):
        self.config = config
        self.event_handler = event_handler

        self.api = self.get_api()
        self.parser = self.get_parser()

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
