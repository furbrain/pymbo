import functools
import typing

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
    def from_elements(cls, types: typing.List[InferredType], maxlen: int) -> "ListType":
        tp = functools.reduce(combine_types, types)
        return cls(tp, maxlen)
