"""
文件
"""
import aiofile

DEFAULT_PATH = "./data/file"


async def write(content, filename):
    """
    保存文件

    :param content: 内容
    :param filename: 文件名
    """
    async with aiofile.async_open(f"{DEFAULT_PATH}/{filename}", mode="w") as file:
        await file.write(content)


async def read(filename) -> str:
    """
    读取文件

    :param filename: 文件名
    :return: 文件内容
    """
    async with aiofile.async_open(f"{DEFAULT_PATH}/{filename}", mode="r") as file:
        return await file.read()
