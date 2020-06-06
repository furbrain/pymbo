from abc import ABCMeta
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
        self.type = None

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

    def definition(self) -> str:
        return ""

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
            return tp
        raise InvalidOperation(f"Attribute {attr} is not a method")

    def set_attr(self, attr: str, tp: "InferredType"):
        self.attrs[attr] = tp

    def add_attr(self, attr: str, typeset: "InferredType"):
        if attr in self.attrs:
            self.attrs[attr] = self.attrs[attr].add_type(typeset)
        else:
            self.attrs[attr] = typeset

    def get_item(self, index_type):
        raise InvalidOperation(f"get item not valid for {self.name}")

    def set_item(self, index_type, value_type):
        raise InvalidOperation(f"Set item not valid for {self.name}")

    def add_item(self, item):
        raise InvalidOperation(f"Set item not valid for {self.name}")

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
        """get the type definitions"""
        return ""

    def get_definitions(self) -> str:
        """this returns all the c code needed to go in a header"""
        return ""

    def get_implementations(self) -> str:
        """this returns all the c code needed to go in a header"""
        return ""


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
