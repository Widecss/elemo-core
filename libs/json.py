# coding: utf-8
# author: Widecss
# Json
import collections
import json


class JSONObject(collections.defaultdict):
    def __init__(self, serializable=None, default_factory=lambda: None, **kwargs):
        super().__init__(default_factory, **kwargs)

        # serialize
        if serializable is None:
            return

        if isinstance(serializable, str):
            dct = json.loads(serializable)
            self.update(dct)

        if isinstance(serializable, dict):
            self.update(serializable)

        if isinstance(serializable, list):
            self.update(serializable)

    def none_to_default(self):
        """当字段的值不存在或者为 None 时，将值设置为定义的默认值"""
        cls = self.__class__
        # default_value
        default_dict = cls.__dict__
        for key, item in default_dict.items():
            if key.startswith("_") or key in self.keys():
                continue
            self[key] = item

        # annotation
        if not hasattr(cls, "__annotations__"):
            return
        default_annotation = cls.__annotations__
        for key, item in default_annotation.items():
            if key.startswith("_") or key in self.keys():
                continue
            self[key] = item()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"


load = json.load
loads = json.loads

dump = json.dump
dumps = json.dumps
