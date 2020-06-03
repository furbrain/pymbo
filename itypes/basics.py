from abc import ABCMeta, abstractmethod

import utils
from exceptions import PymboError


def is_inferred_type(node):
    return isinstance(node, InferredType)

def get_type_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        if obj is None:  # Special case for NoneType which is weird
            return 'None'
        else:
            return '<{}>'.format(type(obj).__name__)

def combine_types(a: "InferredType", b: "InferredType"):
    if a==b:
        return a
    if a == "<int>" and b == "<float>":
        return b
    if b == "<int>" and a == "<float>":
        return a
    return UnknownType()

class InferredType(metaclass=ABCMeta):
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

    def __iter__(self):
        return iter((self,))

    def definition(self) -> str:
        return ""
    def has_attr(self, attr):
        assert(isinstance(attr, str))
        return attr in self.attrs

    def get_attr(self, attr):
        if attr not in self.attrs:
            self.attrs[attr] = UnknownType()
        return self.attrs[attr]

    def set_attr(self, attr, typeset):
        assert(is_inferred_type(typeset))
        self.attrs[attr] = typeset

    def add_attr(self, attr, typeset):
        assert(is_inferred_type(typeset))
        if attr in self.attrs:
            self.attrs[attr] = self.attrs[attr].add_type(typeset)
        else:
            self.attrs[attr] = typeset

    def get_item(self, index_type):
       return UnknownType(),""

    def set_item(self, index_type, value_type):
        raise PymboError(f"Set item not implemented for {self.name}")

    def get_iter(self):
       return UnknownType(),""

    def get_slice_from(self, index):
       return [UnknownType()]

    def add_item(self, item):
        pass
        
    def get_call_return(self, arg_types):
        assert(all(is_inferred_type(x) for x in arg_types))
        if "__call__" in self.attrs:
            return self.attrs['__call__'].get_call_return(arg_types)
        else:
            return UnknownType()

    def get_all_attrs(self):
        return self.attrs.copy()

    def get_star_expansion(self):
        return [UnknownType()]

    def as_c_type(self):
        tp = self.name.strip("<>")
        if tp is None:
            return "void"
        if tp == "None":
            return "void"
        if tp == "int":
            return "int"
        if tp == "float":
            return "double"
        if tp == "str":
            return "char*"
        if tp == "bool":
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