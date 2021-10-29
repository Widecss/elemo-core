"""
Cron 任务处理
"""


class CronExpression:
    """Cron 表达式封装, 默认为 `* * 1 * * ?`

    {秒数} {分钟} {小时} {日期} {月份} {星期} {年份(可为空)}"""

    def __init__(self, expr="* * 1 * * ?"):
        self._expr: str = expr

    @property
    def interval(self):
        raise NotImplementedError("TODO")

    @property
    def next_start_time(self):
        raise NotImplementedError("TODO")