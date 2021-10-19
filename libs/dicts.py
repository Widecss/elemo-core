"""
builtin tools
"""


def filter_mapping(function_or_none, mapping: dict) -> dict:
    """用于过滤 mapping

    :param function_or_none: 过滤函数, 本身为 None 表示过滤为 None 的值, 返回 True 表示通过
    :param mapping: 用于过滤的 mapping
    :return: 新 mapping
    """
    if function_or_none is None:
        return dict([
            (key, value)
            for key, value in mapping.items()
            if value is not None
        ])
    else:
        return dict([
            (key, value)
            for key, value in mapping.items()
            if function_or_none(key, value)
        ])
