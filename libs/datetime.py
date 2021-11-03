# coding: utf-8
# author: Widecss
import time

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"


class DateFormatFactory:
    def __init__(self):
        self._fmt = ""

    def add_string(self, string: str):
        self._fmt += string
        return self

    def add_year(self):
        self._fmt += "%Y"
        return self

    def add_month(self):
        self._fmt += "%m"
        return self

    def add_day(self):
        self._fmt += "%d"
        return self

    def add_hour(self):
        self._fmt += "%H"
        return self

    def add_minute(self):
        self._fmt += "%M"
        return self

    def add_second(self):
        self._fmt += "%S"
        return self

    def to_format(self):
        return self._fmt


def str_from_datetime() -> str:
    """
    返回当前日期 + 时间字符串

    :return: 日期 + 时间字符串
    """
    return str_from(DEFAULT_DATETIME_FORMAT)


def str_from_date() -> str:
    """
    返回当前日期字符串

    :return: 日期字符串
    """
    return str_from(DEFAULT_DATE_FORMAT)


def str_from_time() -> str:
    """
    返回当前时间字符串

    :return: 时间字符串
    """
    return str_from(DEFAULT_TIME_FORMAT)


def str_from(_format: str, time_array: time.struct_time = None) -> str:
    if time_array is None:
        return time.strftime(_format)
    else:
        return time.strftime(_format, time_array)


def time_from(_format: str = DEFAULT_DATETIME_FORMAT, time_string: str = None) -> time.struct_time:
    """
    将时间字符串解析成对应的时间数组，如果不提供则返回当前时间

    :param time_string: 时间字符串
    :param _format: 时间字符串格式
    :return: 时间数组
    """
    if time_string is None:
        return time.localtime()
    else:
        return time.strptime(time_string, _format)


def timestamp_from(time_array: time.struct_time = None) -> int:
    """
    返回时间数组对应的时间戳，没有提供则返回当前时间

    :param time_array: 时间戳（秒）
    :return: 时间数组
    """
    if time_array is None:
        return int(time.time())
    else:
        return int(time.mktime(time_array))


def time_array_from(timestamp: int = None) -> time.struct_time:
    """
    返回时间戳对应的时间数组，没有提供则返回当前时间

    :param timestamp: 时间戳
    :return: 时间数组
    """
    if timestamp is None:
        return time.localtime()
    else:
        return time.localtime(timestamp)
