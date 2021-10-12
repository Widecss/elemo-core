# coding: utf-8
# author: Widecss


def get_full_name(clz: type):
    """
    获取包括包名在内的完整类名
    source: https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python
    :param clz: 一个类
    :return: 类名
    """
    return f"{clz.__module__}.{clz.__qualname__}"
