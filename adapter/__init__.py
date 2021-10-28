"""
Bot 驱动器
"""
import inspect
from asyncio import Task
from typing import Callable, Dict, Awaitable

from libs import dicts, aio
from tools.chain import (
    MessageNode,
    MessageChain,
    Text, Image, Audio
)

__all__ = ["BotAdapter", "BotEventType", "BotEvent", "BotApi", "BotEventParser"]


class BotEventType:
    """Bot 事件类型"""

    BotNoticeMessage = "BotNoticeMessage"
    """提示消息"""

    BotRequestMessage = "BotRequestMessage"
    """请求消息"""

    BotGroupCommand = "BotGroupCommand"
    """群组指令"""

    BotFriendCommand = "BotFriendCommand"
    """私人指令"""

    BotGroupMessage = "BotGroupMessage"
    """群组消息"""

    BotFriendMessage = "BotFriendMessage"
    """私人消息"""

    BotUnknownTypeMessage = "BotUnknownTypeMessage"
    """未知类型消息"""


class BotEvent:
    """Bot 事件"""

    @property
    def timestamp(self) -> str:
        """事件类型"""
        raise NotImplementedError()

    @property
    def type(self) -> BotEventType:
        """事件类型"""
        raise NotImplementedError()

    @property
    def sender_original_id(self) -> str:
        """发送者的原始 id"""
        raise NotImplementedError()

    @property
    def sender_id(self) -> str:
        """发送者 id"""
        return self._package_original_id(self.sender_original_id)

    @property
    def sender_name(self) -> str:
        """发送者名称"""
        raise NotImplementedError()

    @property
    def group_original_id(self) -> str:
        """群组的原始 id, 在非群组消息时会抛出异常"""
        raise NotImplementedError()

    @property
    def group_id(self) -> str:
        """群组 id, 在非群组消息时会抛出异常"""
        return self._package_original_id(self.group_original_id)

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

    def _package_original_id(self, original_id):
        return f"{self.__class__.__name__.lower()}_{original_id}"


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
        """
        回复消息

        :param message_chain: 消息链
        """
        raise NotImplementedError()


BotEventHandlerFunction = Callable[[BotApi, BotEvent], Awaitable[None]]


class BotAdapter:
    """Bot客户端的适配器

    on_start() 将在启动时调用, 用于开启事件接收
    on_close() 将在关闭时调用, 用于关闭事件接收

    handle_event() 传入事件数据以处理事件
    """

    config: Dict = None
    """一些配置"""

    _event_handler: BotEventHandlerFunction = None
    """事件处理器"""

    _api: BotApi = None
    """Bot 接口"""

    _parser: BotEventParser = None
    """Bot 事件解析器"""

    _on_start_task: Task = None
    """Bot 事件循环任务"""

    def __init__(self, config, event_handler):
        self.config = config
        self._event_handler = event_handler

    async def handle_event(self, event_data):
        """将事件传入以进行处理

        :param event_data: 事件数据, 将直接传给 BotEventParser.load()
        """
        if self._event_handler:
            await self._event_handler(
                self._api,
                self._parser.load(event_data)
            )

    async def create_api(self) -> BotApi:
        """创建自定义的 BotApi

        :return: 自定义的 BotApi
        """
        raise NotImplementedError()

    async def create_parser(self) -> BotEventParser:
        """创建自定义的 BotEventParser

        :return: 自定义的 BotEventParser
        """
        raise NotImplementedError()

    async def on_event_loop(self):
        """启动时"""
        raise NotImplementedError()

    async def on_close(self):
        """关闭时"""
        raise NotImplementedError()

    async def start(self):
        self._api = await self.create_api()
        self._parser = await self.create_parser()
        self._on_start_task = aio.add_task_to_event_loop(self.on_event_loop())

    async def close(self):
        await self.on_close()
        self._on_start_task.cancel()
