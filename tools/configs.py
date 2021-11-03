"""
配置
"""
import logging

import aiofile
import yaml

from libs import clazz


class BaseConfig:
    def __init__(self, content: dict):
        self.content: dict = content


class AdapterConfig(BaseConfig):
    pass


class ModuleConfig(BaseConfig):
    pass


class ServiceConfig(BaseConfig):
    pass


class NetworkConfig(BaseConfig):
    pass


class BotConfig:
    adapter: AdapterConfig
    module: ModuleConfig
    service: ServiceConfig
    network: NetworkConfig

    def __init__(self, content: dict):
        clz_list: dict = clazz.search_class_in_globals("Config", globals())
        key: str
        for key, value in content.items():
            clz_name = f"{key[0].upper()}{key[1:]}Config"
            try:
                clz = clz_list[clz_name]
                self.__dict__[key] = clz(value)
            except KeyError:
                logging.warning(f"configs 中未定义名为 {clz_name} 的配置类, 已跳过加载配置 {key}")


async def load(_path) -> BotConfig:
    async with aiofile.async_open(_path) as file:
        text = await file.read()
        content = yaml.load(text, Loader=yaml.Loader)
        return BotConfig(content)
