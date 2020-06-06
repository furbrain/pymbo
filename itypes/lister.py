import functools
import os
import typing
from textwrap import dedent

from itypes import InferredType, combine_types
from itypes.functions import NativeMethod


class Lister(InferredType):
    pass_by_value = False

    def __init__(self, tp: InferredType, maxlen: int):
        from itypes.typedb import TypeDB
        super().__init__()
        self.tp = tp
        self.maxlen = maxlen
        self.name = f"[{tp.name}:{maxlen}]"
        self.functions = set()
        c_func_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../c_functions"))
        with open(os.path.join(c_func_dir, "lists.py")) as f:
            c_data = eval(f.read(), {"__builtins__": None})
        self.definition = c_data["def"]
        self.c_funcs = {}
        for name, func in c_data["methods"].items():
            vals = {name: dedent(val.format(**self.get_c_function_dict())) for name, val in func.items()}
            args = [TypeDB.get_type_by_name(arg.strip()) for arg in vals['args'].split(',')]
            retval = TypeDB.get_type_by_name(vals['retval'])
            self.c_funcs[name] = NativeMethod(f'{self.prefix()}__{name}', args, retval, vals['def'], vals['imp'])

    def get_c_function_dict(self):
        return {
            "tp": self.tp.as_c_type(),
            "maxlen": self.maxlen,
            "prefix": self.prefix()
        }

    def get_type_def(self) -> str:
        return dedent(self.definition.format(**self.get_c_function_dict()))

    def get_definitions(self):
        return "".join(self.c_funcs[func].definition for func in self.functions)

    def get_implementations(self):
        return "".join(self.c_funcs[func].implementation for func in self.functions)

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
