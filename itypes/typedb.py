from itypes import InferredType
from typing import Optional, Sequence, Dict

from itypes.lister import Lister
from . import basics
from old_itypes import classes

BUILTIN_TYPES = (int, bool, float, str)

def get_builtins():
    types: Dict[str, InferredType] = {}
    for tp in BUILTIN_TYPES:
        types[tp.__name__] = InferredType.from_type(tp)
        types["None"] = InferredType.from_type(type(None))
    types["None"].name = "None"
    return types

class TypeDB:
    types: Dict[str, InferredType] = get_builtins()

    @classmethod
    def get_list(cls, elements: Sequence[InferredType], maxlen: Optional[int] = None):
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
    def classiter(self):
        return iter(self.types.values())

def get_type_by_value(value) -> basics.InferredType:
    return TypeDB.get_type_by_value(value)

def get_type_by_name(text: str) -> basics.InferredType:
    return TypeDB.get_type_by_name(text)
