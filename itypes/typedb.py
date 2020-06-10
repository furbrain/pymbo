from typing import Optional, Dict, List

from itypes import InferredType
from itypes.lister import Lister
from . import basics
from .primitives import IntType, FloatType


def get_builtins():
    types: Dict[str, InferredType] = {'int': IntType(), 'float': FloatType()}
    for tp in (bool, str):
        types[tp.__name__] = InferredType.from_type(tp)
    types["None"] = InferredType.from_type(type(None))
    types["None"].name = "None"
    types["bytes"] = types["str"]
    return types


class TypeDB:
    types: Dict[str, InferredType] = get_builtins()

    @classmethod
    def get_list(cls, elements: List[InferredType], maxlen: Optional[int] = None):
        if maxlen is None:
            maxlen = 40
        tp = Lister.from_elements(elements, maxlen)
        return cls.types.setdefault(tp.as_c_type(), tp)

    @classmethod
    def get_type_by_name(cls, text: str) -> basics.InferredType:
        if text not in cls.types:
            raise AttributeError('Unknown type {}'.format(text))
        return cls.types[text]

    @classmethod
    def get_type_by_value(cls, value):
        type_name = basics.get_type_name(value)
        return cls.get_type_by_name(type_name)

    @classmethod
    def classiter(cls):
        return iter(cls.types.values())

    @classmethod
    def reset(cls):
        cls.types = get_builtins()
