"""
程序入口
"""

from libs import aio


class ContextManager:
    def __init__(self):
        pass

    async def _loop(self):
        pass

    def loop(self):
        aio.run(self._loop())


def main():
    context = ContextManager()
    context.loop()


if __name__ == '__main__':
    main()
