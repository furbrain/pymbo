import os
from abc import ABCMeta
from textwrap import dedent
from typing import TYPE_CHECKING

from exceptions import InvalidOperation, StaticTypeError

if TYPE_CHECKING:  # pragma: no cover
    from itypes.functions import FunctionType

def get_type_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        if obj is None:  # Special case for NoneType which is weird
            return 'None'
        else:
            return '{}'.format(type(obj).__name__)


def combine_types(a: "InferredType", b: "InferredType"):
    if a.can_coerce_from(b):
        return a
    if b.can_coerce_from(a):
        return b
    raise StaticTypeError(f"Incompatible types: {a} {b}")

# noinspection PyMethodMayBeStatic
class InferredType(metaclass=ABCMeta):
    pass_by_value = True

    def __init__(self):
        self.attrs = {}
        self.items = None
        self.name = ""
        self.definition = ""
        self.type = None
        self.functions = set()
        self.methods_loaded = False
        self.spec_file = ""
        self.c_type = ""

    def __str__(self):
        return self.name

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
        return self.c_type

    def load_methods(self):
        if self.methods_loaded or self.spec_file == "":
            return
        from .functions import NativeMethod, InlineNativeMethod
        c_func_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../c_functions"))
        with open(os.path.join(c_func_dir, self.spec_file)) as f:
            c_data = eval(f.read(), {"__builtins__": None})
        self.definition = c_data["def"]
        self.definition = eval(f'f"""{self.definition}"""')
        for name, func in c_data["methods"].items():
            vals, args, retval = self.get_vals_args_and_retval(func)
            self.attrs[name] = NativeMethod(f'{self.prefix()}__{name}', args, retval, vals['def'], vals['imp'])
        for name, func in c_data["inlines"].items():
            vals, args, retval = self.get_vals_args_and_retval(func)
            self.attrs[name] = InlineNativeMethod(f'{self.prefix()}__{name}', args, retval, func['template'])
        self.methods_loaded = True

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
        self.load_methods()
        return attr in self.attrs

    def get_attr(self, attr: str) -> "InferredType":
        self.load_methods()
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
        self.load_methods()
        self.attrs[attr] = tp

    def add_attr(self, attr: str, typeset: "InferredType"):
        self.load_methods()
        if attr in self.attrs:
            self.attrs[attr] = self.attrs[attr].add_type(typeset)
        else:
            self.attrs[attr] = typeset

    def get_all_attrs(self):
        return self.attrs.copy()

    def get_type_def(self) -> str:
        self.load_methods()
        return self.definition

    def get_definitions(self):
        funcs_with_defs = [self.attrs[f] for f in self.functions if hasattr(self.attrs[f], "definition")]
        return "".join(f.definition for f in funcs_with_defs)

    def get_implementations(self):
        funcs_with_imps = [self.attrs[f] for f in self.functions if hasattr(self.attrs[f], "implementation")]
        return "".join(f.implementation for f in funcs_with_imps)

    def can_coerce_from(self, other: "InferredType") -> bool:
        return self == other
