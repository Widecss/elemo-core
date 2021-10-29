"""
文件
"""
import os

import aiofile

from libs import clazz

DEFAULT_FILE_PATH = "./data/file"
PUBLIC_DIR = "public"


async def write(content, filename, cls=None) -> int:
    """
    保存文件

    :param content: 内容
    :param filename: 文件名
    :param cls: 文件从属的类, 不提供将保存到公共文件夹
    """
    full_path = _ensure_class_dir(cls)

    async with aiofile.async_open(f"{full_path}/{filename}", mode="w") as file:
        return await file.write(content)


async def read(filename, cls=None) -> str:
    """
    读取文件

    :param filename: 文件名
    :param cls: 文件从属的类, 不提供将保存到公共文件夹
    :return: 文件内容
    """
    full_path = _ensure_class_dir(cls)

    async with aiofile.async_open(f"{full_path}/{filename}", mode="r") as file:
        return await file.read()


def _ensure_class_dir(cls):
    if cls:
        name = clazz.get_full_name(cls)
    else:
        name = PUBLIC_DIR

    path = name.replace(".", "/")
    full_path = f"{DEFAULT_FILE_PATH}/{path}"

    os.makedirs(full_path, exist_ok=True)
    return full_path


class Filer:

    async def write(self, content, filename) -> int:
        return await write(content, filename, self.__class__)

    async def read(self, filename) -> str:
        return await read(filename, self.__class__)
