"""
网络请求处理
"""
import aiohttp

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=30)
"""默认超时"""

DEFAULT_PROXY = f"http://127.0.0.1:7890"
"""默认代理"""


class Response:
    _encoding: str = "utf-8"

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        self._encoding = value

    async def json(self) -> dict:
        raise NotImplementedError()

    async def text(self) -> str:
        raise NotImplementedError()

    async def content(self) -> bytes:
        raise NotImplementedError()


class AioHttpResponse(Response):

    def __init__(self, raw: aiohttp.ClientResponse):
        self.raw = raw

    async def json(self) -> dict:
        return await self.raw.json(encoding=self.encoding)

    async def text(self) -> str:
        return await self.raw.text(encoding=self.encoding)

    async def content(self) -> bytes:
        return await self.raw.read()


async def get(
        url: str,
        params: dict = None,
        cookies: dict = None,
        headers: dict = None
) -> Response:
    """发送 GET 请求"""
    async with aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            timeout=DEFAULT_TIMEOUT
    ) as session:
        async with session.get(
                url=url,
                params=params,
                proxy=DEFAULT_PROXY
        ) as res:
            return AioHttpResponse(res)


async def post(
        url: str,
        params: dict = None,
        data: dict = None,
        cookies: dict = None,
        headers: dict = None
) -> Response:
    """发送 POST 请求"""
    async with aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            timeout=DEFAULT_TIMEOUT
    ) as session:
        async with session.post(
                url=url,
                data=data,
                params=params,
                proxy=DEFAULT_PROXY
        ) as res:
            return AioHttpResponse(res)


