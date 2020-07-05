import functools
from typing import Union, List

from itypes import InferredType, combine_types


class ListType(InferredType):
    pass_by_value = False

    def __init__(self, tp: InferredType, maxlen: int):
        super().__init__()
        self.tp = tp
        self.maxlen = maxlen
        self.name = f"[{tp.name}:{maxlen}]"
        self.spec_file = "lists.py"
        self.c_type = self.prefix()

    def prefix(self):
        return f"list{self.maxlen:d}__{self.tp.c_type}"

    def as_literal(self, values: str):
        return f"({self.c_type}){{{len(values)}, {{{', '.join(values)}}}}}"

    @classmethod
    def from_elements(cls, types: List[InferredType], maxlen: int) -> Union["ListType", "EmptyList"]:
        if len(types) == 0:
            return EmptyList()
        if len(types) == 1:
            tp = types[0]
        else:
            tp = functools.reduce(combine_types, types)
        return cls(tp, maxlen)


class EmptyList(InferredType):
    def __init__(self):
        super().__init__()
        self.name = "Empty List"

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def as_literal(self, vals):
        return "{0}"
