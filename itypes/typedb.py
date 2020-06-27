from typing import Optional, Dict, List

from exceptions import InvalidOperation
from itypes import InferredType
from itypes.lists import ListType
from . import basics
from .primitives import IntType, FloatType, BoolType, NoneType
from .strings import StrType


def get_builtins():
    types: Dict[str, InferredType] = {'int': IntType(),
                                      'float': FloatType(),
                                      'bool': BoolType(),
                                      'None': NoneType()}
    return types


class TypeDB:
    types: Dict[str, InferredType] = get_builtins()

    @classmethod
    def get_list(cls, elements: List[InferredType], maxlen: Optional[int] = None):
        if maxlen is None:
            maxlen = 40
        tp = ListType.from_elements(elements, maxlen)
        return cls.types.setdefault(tp.name, tp)

    @classmethod
    def get_string(cls, maxlen: Optional[int] = None):
        if maxlen is None:
            maxlen = 40
        tp = StrType(maxlen)
        return cls.types.setdefault(tp.name, tp)

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
    def reset(cls):
        cls.types = get_builtins()

    @classmethod
    def add_type(cls, tp: InferredType):
        if tp.name in cls.types:
            raise InvalidOperation("Duplicate type {tp.name}")
        cls.types[tp.name] = tp
