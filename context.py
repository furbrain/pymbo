from typing import Dict, Optional

from itypes import InferredType
class Var:
    def __init__(self, tp: InferredType, is_pointer=False, is_exported=False, is_arg=False):
        self.tp = tp
        self.is_pointer = is_pointer
        self.is_exported = is_exported
        self.is_arg = is_arg

class Context:
    def __init__(self, parent: Optional["Context"] = None, fname="<string>"):
        self.fname = fname
        self.parent = parent
        self.dct : Dict[str, Var] = {}

    def __setitem__(self, key: str, value: Var):
        self.dct[key] = value

    def __getitem__(self, key:str):
        if key in self.dct:
            return self.dct[key]
        if self.parent is not None:
            return self.parent[key]
        raise KeyError

    def __contains__(self, key:str):
        if key in self.dct:
            return True
        if self.parent is not None:
            return key in self.parent
        else:
            return False

    def locals(self):
        return self.dct.items()

