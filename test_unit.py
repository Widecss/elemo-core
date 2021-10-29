"""
单元测试
"""
import asyncio
import json
import unittest

from adapter.go_cqhttp import (
    GoCQHttpAdapter,
    GoCQHttpApi,
    GoCQHttpEvent,
    GoCQHttpEventType
)
from libs import aio


class GoCQHttpTest(unittest.TestCase):

    def test_ws_connection(self):
        """WebSocket 连接测试"""

        async def event_handler(api: GoCQHttpApi, event_data: GoCQHttpEvent):
            self.assertTrue(isinstance(api, GoCQHttpApi), "api 不是一个 GoCQHttpApi")

            self.assertTrue(isinstance(event_data, GoCQHttpEvent), "event_data 不是一个 GoCQHttpEvent")
            self.assertTrue("raw" in event_data.__dict__, "event_data 没有 raw 属性")
            self.assertTrue(isinstance(event_data.raw, dict), "event_data.raw 不是一个 dictionary")
            print(json.dumps(event_data.raw, indent=4))

            self.assertTrue("post_type" in event_data.raw.keys(), "event_data 里面没有 post_type 字段")

        adapter = GoCQHttpAdapter(
            config=None,
            event_handler=event_handler
        )

        async def main():
            async def close():
                await asyncio.sleep(5)
                await adapter.close()

            await aio.create_task_and_start(adapter.start())
            # aio.add_task_to_event_loop(close())
            await asyncio.sleep(10)

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("测试结束")

    def test_message(self):
        """消息测试"""

        async def event_handler(api: GoCQHttpApi, event_data: GoCQHttpEvent):
            self.assertTrue(isinstance(event_data, GoCQHttpEvent), "event_data 不是一个 dictionary")
            if event_data.type in [
                GoCQHttpEventType.GoCQHttpHeartbeat,
                GoCQHttpEventType.GoCQHttpLifecycle
            ]:
                return
            print(json.dumps(event_data.raw, indent=4))

        adapter = GoCQHttpAdapter(
            config=None,
            event_handler=event_handler
        )

        async def main():
            await adapter.start()
            while True:
                await asyncio.sleep(1)

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("测试结束")


class CommandTest:
    pass


class ServiceTest:
    pass


class ToolTest:
    def filer_test(self):
        pass


class LibTest:
    pass
