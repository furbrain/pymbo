import functools
import typing

from itypes import InferredType, combine_types
from textwrap import dedent
class Lister(InferredType):
    def __init__(self, tp: InferredType, maxlen: int):
        self.tp = tp
        self.maxlen = maxlen
        self.name = f"[{tp.name}:{maxlen}]"
        self.functions = set()

    def prefix(self):
        return f"list{self.maxlen:d}__{self.tp.as_c_type()}"

    def as_c_type(self):
        """get the c_type for use in function params etc"""
        return f"struct {self.prefix()}"

    def definition(self):
        """get the code to define this as a struct"""
        return dedent(f"""
            {self.as_c_type()} {{
                {self.tp.as_c_type()} items[{self.maxlen}];
                int count;
            }}; 
        """)

    def as_literal(self, values: str):
        return f"({self.as_c_type()}){{{len(values)}, {{{', '.join(values)}}}}}"

    @classmethod
    def from_elements(cls, types: typing.List[InferredType], maxlen: int):
        tp = functools.reduce(combine_types, types)
        return cls(tp, maxlen)

    def get_item(self, index_type):
        if index_type!="<int>":
            raise ValueError("Index type should be an integer")
        self.functions.add("get_item")
        return self.tp, f"{self.prefix()}__get_item"


