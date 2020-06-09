import functools
import typing

from itypes import InferredType, combine_types


class Lister(InferredType):
    pass_by_value = False

    def __init__(self, tp: InferredType, maxlen: int):
        super().__init__()
        self.tp = tp
        self.maxlen = maxlen
        self.name = f"[{tp.name}:{maxlen}]"
        self.functions = set()
        self.load_methods("lists.py")

    def prefix(self):
        return f"list{self.maxlen:d}__{self.tp.as_c_type()}"

    def as_c_type(self):
        """get the c_type for use in function params etc"""
        return f"struct {self.prefix()}"

    def as_literal(self, values: str):
        return f"({self.as_c_type()}){{{len(values)}, {{{', '.join(values)}}}}}"

    @classmethod
    def from_elements(cls, types: typing.List[InferredType], maxlen: int) -> "Lister":
        tp = functools.reduce(combine_types, types)
        return cls(tp, maxlen)

    def get_attr(self, attr: str):
        if attr in self.c_funcs:
            self.functions.add(attr)
            return self.c_funcs[attr]
        return super().get_attr(attr)
