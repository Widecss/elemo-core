"""
单元测试
"""
import asyncio
import json
import sys
import unittest

from adapter.go_cqhttp import GoCQHttpAdapter, GoCQHttpApi, GoCQHttpEvent


class GoCQHttpTest(unittest.TestCase):
    """测试适配器, 保证其正常接收和发送消息"""

    def test_ws_connection(self):
        async def event_handler(api: GoCQHttpApi, event_data: GoCQHttpEvent):
            print(json.dumps(event_data.raw, indent=4))
            self.assertTrue(isinstance(api, GoCQHttpApi), "event_data 不是一个 dictionary")

            self.assertTrue(isinstance(event_data, GoCQHttpEvent), "event_data 不是一个 dictionary")
            self.assertTrue("raw" in event_data.__dict__, "event_data 没有 raw 属性")

            self.assertTrue(isinstance(event_data.raw, dict), "event_data.raw 不是一个 dictionary")
            self.assertTrue("post_type" in event_data.raw.keys(), "event_data 里面没有 post_type 字段")

        adapter = GoCQHttpAdapter()
        adapter.event_handler = event_handler
        try:
            asyncio.run(adapter.on_start())
        except KeyboardInterrupt:
            print("测试结束")


class CommandTest:
    """测试指令模块, 保证其正常处理事件和返回结果"""


class ServiceTest:
    """测试服务模块, 保证其正常读取和保存数据"""
