import os
from abc import ABCMeta
from textwrap import dedent
from typing import TYPE_CHECKING

import utils
from exceptions import InvalidOperation

if TYPE_CHECKING:  # pragma: no cover
    from itypes.functions import FunctionType


def can_promote(src: "InferredType", dest: "InferredType"):
    if src == dest:
        return True
    if src == "int":
        if dest == "float":
            return True
    return False


def get_type_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        if obj is None:  # Special case for NoneType which is weird
            return 'None'
        else:
            return '{}'.format(type(obj).__name__)


def combine_types(a: "InferredType", b: "InferredType"):
    if a == b:
        return a
    if a == "int" and b == "float":
        return b
    if b == "int" and a == "float":
        return a
    return UnknownType()


# noinspection PyMethodMayBeStatic
class InferredType(metaclass=ABCMeta):
    pass_by_value = True

    @classmethod
    def from_type(cls, object_type):
        self = cls()
        self.type = object_type
        self.name = get_type_name(object_type)
        return self

    def __init__(self):
        self.attrs = {}
        self.items = None
        self.name = ""
        self.docstring = ""
        self.definition = ""
        self.type = None
        self.functions = set()
        self.c_funcs = {}

    @utils.do_not_recurse('...')
    def __str__(self):
        return self.name

    @utils.do_not_recurse('...')
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, InferredType):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance(other, type):
            return self.type == other
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.name)

    def prefix(self):
        return self.as_c_type()

    def load_methods(self, fname: str):
        from .functions import NativeMethod, InlineNativeMethod
        c_func_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../c_functions"))
        with open(os.path.join(c_func_dir, fname)) as f:
            c_data = eval(f.read(), {"__builtins__": None})
        self.definition = c_data["def"]
        self.definition = eval(f'f"""{self.definition}"""')
        self.c_funcs = {}
        for name, func in c_data["methods"].items():
            vals, args, retval = self.get_vals_args_and_retval(func)
            self.c_funcs[name] = NativeMethod(f'{self.prefix()}__{name}', args, retval, vals['def'], vals['imp'])
        for name, func in c_data["inlines"].items():
            vals, args, retval = self.get_vals_args_and_retval(func)
            self.c_funcs[name] = InlineNativeMethod(f'{self.prefix()}__{name}', args, retval, func['template'])

    def get_vals_args_and_retval(self, func):
        from itypes.typedb import TypeDB
        vals = {name: dedent(eval(f'f"""{val}"""', {'self': self})) for name, val in func.items() if
                name != "template"}
        args = [arg.strip() for arg in vals['args'].split(',')]
        if args != ['']:
            args = [TypeDB.get_type_by_name(arg) for arg in args]
        else:
            args = []
        retval = TypeDB.get_type_by_name(vals['retval'])
        return vals, args, retval

    def has_attr(self, attr: str) -> bool:
        return attr in self.attrs

    def get_attr(self, attr: str) -> "InferredType":
        if attr not in self.attrs:
            raise InvalidOperation(f"Get attr {attr} not valid for {self.name}")
        return self.attrs[attr]

    def get_method(self, attr: str) -> "FunctionType":
        from itypes.functions import FunctionType
        tp = self.get_attr(attr)
        if isinstance(tp, FunctionType):
            self.functions.add(attr)
            return tp
        raise InvalidOperation(f"Attribute {attr} is not a method")

    def set_attr(self, attr: str, tp: "InferredType"):
        self.attrs[attr] = tp

    def add_attr(self, attr: str, typeset: "InferredType"):
        if attr in self.attrs:
            self.attrs[attr] = self.attrs[attr].add_type(typeset)
        else:
            self.attrs[attr] = typeset

    def get_all_attrs(self):
        return self.attrs.copy()

    def as_c_type(self):
        if self.name is None:
            return "void"
        if self.name == "None":
            return "void"
        if self.name == "int":
            return "int"
        if self.name == "float":
            return "double"
        if self.name == "str":
            return "char*"
        if self.name == "bool":
            return "bool"
        raise NotImplementedError("Not able to create c type for %s" % self.name)

    def get_type_def(self) -> str:
        return self.definition

    def get_definitions(self):
        funcs_with_defs = [self.c_funcs[f] for f in self.functions if hasattr(self.c_funcs[f], "definition")]
        return "".join(f.definition for f in funcs_with_defs)

    def get_implementations(self):
        funcs_with_imps = [self.c_funcs[f] for f in self.functions if hasattr(self.c_funcs[f], "implementation")]
        return "".join(f.implementation for f in funcs_with_imps)


class UnknownType(InferredType):
    def __init__(self, name=None):
        super().__init__()
        if name:
            self.name = "Unknown: %s" % name
            self.type = name
        else:
            self.name = "Unknown"
            self.type = ""
        raise ValueError("Shouldn't get here")
