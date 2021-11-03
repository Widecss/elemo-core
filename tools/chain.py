"""
简易的消息链
"""

__all__ = ["MessageChain", "MessageNode", "Text", "Image", "Audio"]


class MessageChain:
    _chain: list["MessageNode"]

    def __init__(self, *args):
        self._chain = [*args]

    def __add__(self, other):
        if isinstance(other, MessageNode):
            self._chain += [other]
        if isinstance(other, MessageChain):
            self._chain += other.chain
        return self

    @property
    def chain(self) -> list:
        return self._chain

    def __str__(self):
        return str(" ")


class MessageNode:
    content = None

    def __iadd__(self, other):
        raise TypeError("unsupported operand type(s) for +=: try something like 'chain = node + node'")

    def __add__(self, other):
        return MessageChain(self) + other

    def __str__(self):
        return str(self.content)


class Text(MessageNode):
    def __init__(self, text: str = ""):
        self.content = text

    def change_text(self, text):
        self.content = text

    def __iadd__(self, other):
        if isinstance(other, str):
            self.content += other
            return self
        else:
            return super().__iadd__(other)

    def __radd__(self, other):
        print(other)

    def __add__(self, other):
        if isinstance(other, str):
            self.content += other
            return self
        else:
            return super().__add__(other)


class Image(MessageNode):
    def __init__(self, url_or_path=None):
        self.content = url_or_path


class Audio(MessageNode):
    def __init__(self, url_or_path=None):
        self.content = url_or_path
