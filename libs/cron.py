"""
Cron 任务处理
"""


class CronExpression:
    """Cron 表达式封装, 默认为 ``* * 1 * * ?``

    {秒数} {分钟} {小时} {日期} {月份} {星期} {年份(可为空)}"""

    def __init__(self, expr="* * 1 * * ?"):
        self._expr: str = expr

        self._separate()

    def _separate(self):
        raise NotImplementedError("TODO")

    @property
    def interval(self) -> int:
        """
        间隔

        :return: 返回间隔的秒数
        """
        raise NotImplementedError("TODO")

    @property
    def next_time(self) -> int:
        """
        下次

        :return: 返回下次匹配的时间
        """
        raise NotImplementedError("TODO")

    def match(self, _time) -> bool:
        """
        匹配时间

        :param _time: 时间戳
        :return: 是否匹配成功
        """
        raise NotImplementedError("TODO")
