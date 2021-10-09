"""
主文件
"""
from libs import aio


async def main():
    print("Hello, Elemo!")


if __name__ == '__main__':
    aio.run(main())
