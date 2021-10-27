"""
文件
"""
import os

import aiofile

from libs import clazz

DEFAULT_FILE_PATH = "./data/file"


class Filer:

    async def write(self, content, filename):
        """
        保存文件

        :param content: 内容
        :param filename: 文件名
        """
        full_path = _ensure_class_dir(self.__class__)

        async with aiofile.async_open(f"{full_path}/{filename}", mode="w") as file:
            await file.write(content)

    async def read(self, filename) -> str:
        """
        读取文件

        :param filename: 文件名
        :return: 文件内容
        """
        full_path = _ensure_class_dir(self.__class__)

        async with aiofile.async_open(f"{full_path}/{filename}", mode="r") as file:
            return await file.read()


def _ensure_class_dir(cls):
    name = clazz.get_full_name(cls)
    path = name.replace(".", "/")
    full_path = f"{DEFAULT_FILE_PATH}/{path}"

    os.makedirs(full_path, exist_ok=True)

    return full_path
