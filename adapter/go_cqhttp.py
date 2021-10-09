from . import BaseAdapter


class GoCQHTTPAdapter(BaseAdapter):
    async def data_receiver(self, session):
        pass
        # async with session.ws_connect('http://127.0.0.1:6700/') as ws:
        #     async for response in ws:
        #         if response.type == aiohttp.WSMsgType.TEXT:
        #             json.loads(response.json)
        #         elif response.type == aiohttp.WSMsgType.ERROR:
        #             print(f"err: {response.data}")

    async def start_event_loop(self) -> None:
        pass
        # async with aiohttp.ClientSession() as session:
        #     await ws_handler(session)
