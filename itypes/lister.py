import functools
import os
import typing

from itypes import InferredType, combine_types
from textwrap import dedent
class Lister(InferredType):
    def __init__(self, tp: InferredType, maxlen: int):
        self.tp = tp
        self.maxlen = maxlen
        self.name = f"[{tp.name}:{maxlen}]"
        self.functions = set()
        c_func_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../c_functions"))
        with open(os.path.join(c_func_dir, "lists.py")) as f:
            self.c_funcs = eval(f.read(), {"__builtins__": None})

    def get_c_function_dict(self):
        return {
            "tp": self.tp.as_c_type(),
            "maxlen": self.maxlen,
            "prefix": self.prefix()
        }
    def get_c_definition(self, func: str):
        return dedent(self.c_funcs[func]['def'].format(**self.get_c_function_dict()))

    def get_c_implementation(self, func: str):
        return dedent(self.c_funcs[func]['imp'].format(**self.get_c_function_dict()))

    def get_type_def(self) -> str:
        return dedent(self.c_funcs["def"].format(**self.get_c_function_dict()))

    def get_definitions(self):
        return "".join([self.get_c_definition(func) for func in self.functions])

    def get_implementations(self):
        return "".join([self.get_c_implementation(func) for func in self.functions])

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

    def get_item(self, index_type):
        if index_type!="<int>":
            raise ValueError("Index type should be an integer")
        self.functions.add("get_item")
        return self.tp, f"{self.prefix()}__get_item"

    def set_item(self, index_type, value_type):
        if index_type != "<int>":
            raise ValueError("Index type should be an integer")
        if value_type != self.tp:
            raise ValueError(f"Assigned value {value_type} should be {self.tp}")
        self.functions.add("set_item")
        return f"{self.prefix()}__set_item"
