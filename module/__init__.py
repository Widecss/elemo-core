from adapter import BotAdapter, BotEvent


class BotModule:
    allow_type = []
    """允许使用此模块的消息类型"""

    is_admin_module = False
    """是否为管理员模块"""

    async def handle(self, bot: BotAdapter, event: BotEvent) -> bool:
        """
        事件处理函数, 将在每一次触发事件时调用
        :param bot: 事件对应的 bot 端
        :param event: 事件
        :return: 返回 True 表示拦截该消息, 不再继续传给其他模块处理
        """
        raise NotImplementedError()
