from typing import Dict, Optional

from exceptions import StaticTypeError
from itypes import InferredType, can_promote


class Code:
    def __init__(self, tp: Optional[InferredType], is_pointer=False, is_exported=False, is_arg=False, code=""):
        self.tp = tp
        self.is_pointer = is_pointer
        self.is_exported = is_exported
        self.is_arg = is_arg
        self.code = code

    def as_pointer(self):
        if self.is_pointer:
            return self
        else:
            return Code(tp=self.tp, is_pointer=True, code=f"&({self.code})")

    def as_value(self):
        if self.is_pointer:
            return Code(tp=self.tp, is_pointer=False, code=f"*({self.code})")
        else:
            return self

    def assign_type(self, tp, additional_text=""):
        if self.tp is None:
            self.tp = tp
            return
        if can_promote(tp, self.tp):
            return
        elif can_promote(self.tp, tp):
            self.tp = tp
            return
        # not been able to match types - raise error
        raise StaticTypeError(f"Assigning {tp} to {self.tp}{additional_text}")

    def as_function_arg(self):
        if self.tp.pass_by_value:
            return self.as_value()
        else:
            return self.as_pointer()

class Context:
    def __init__(self, parent: Optional["Context"] = None, fname="<string>"):
        self.fname = fname
        self.parent = parent
        self.dct: Dict[str, Code] = {}

    def __setitem__(self, key: str, value: Code):
        self.dct[key] = value

    def __getitem__(self, key: str) -> Code:
        if key in self.dct:
            return self.dct[key]
        if self.parent is not None:
            return self.parent[key]
        raise KeyError

    def __contains__(self, key: str) -> bool:
        if key in self.dct:
            return True
        if self.parent is not None:
            return key in self.parent
        else:
            return False

    def setdefault(self, key: str, default: Code) -> Code:
        if key not in self:
            self[key] = default
        return self[key]

    def locals(self):
        return self.dct.items()
