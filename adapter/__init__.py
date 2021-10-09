"""
Bot 驱动器
"""
from queue import Queue


class EventData:
    pass


class EventQueue(Queue):
    pass


class BaseAdapter:
    def __init__(self, event_queue: EventQueue):
        self._queue: EventQueue = event_queue

    async def start_event_loop(self) -> None:
        raise NotImplementedError()
