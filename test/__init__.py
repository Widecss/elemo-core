"""
单元测试
"""
import asyncio
import unittest

from adapter.go_cqhttp import GoCQHttpAdapter


class GoCQHttpTest(unittest.TestCase):
    """测试适配器, 保证其正常接收和发送消息"""

    def test_ws_connection(self):
        def event_handler(event_data: dict):
            print(event_data)
            self.assertTrue(isinstance(event_data, dict), "event_data 不是一个 dictionary")
            self.assertTrue("time" in event_data.keys(), "event_data 里面没有 time 字段")

        adapter = GoCQHttpAdapter()
        adapter.event_handler = event_handler
        try:
            asyncio.run(adapter.start())
        except KeyboardInterrupt:
            print("测试结束")


class CommandTest:
    """测试指令模块, 保证其正常处理事件和返回结果"""


class ServiceTest:
    """测试服务模块, 保证其正常读取和保存数据"""
