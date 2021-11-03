"""
类操作
"""
import inspect


def get_full_name(clz: type):
    """
    获取包括包名在内的完整类名
    source: https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python

    :param clz: 一个类
    :return: 类名
    """
    return f"{clz.__module__}.{clz.__qualname__}"


def search_class_in_globals(word: str, gls: dict):
    """
    在 globals() 中搜索类

    :param word: 关键词
    :param gls: globals()
    :return: 搜索结果列表
    """
    return dict([(key, value) for key, value in gls.items() if all([
        inspect.isclass(value),
        word in key
    ])])
