"""
配置
"""


class BaseConfig:
    def __init__(self):
        pass


class BotConfig(BaseConfig):
    pass


class AdapterConfig(BaseConfig):
    pass


class ModuleConfig(BaseConfig):
    pass


class ServiceConfig(BaseConfig):
    pass


class ConfigLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        pass

    def reload(self):
        pass
